import os
from typing import Annotated
from langchain_core.tools import StructuredTool
from langchain_core.vectorstores import VectorStore
from langchain_openai import ChatOpenAI
from pydantic import Field
from langchain_core.messages import (
    SystemMessage,
    ToolMessage,
    trim_messages,
)

from langgraph.checkpoint.base import BaseCheckpointSaver

from rag_pipeline.utils import limit_calls
from langchain_core.tools.base import InjectedToolCallId
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import InjectedState, ToolNode, tools_condition
from langgraph.types import Command
from pydantic import BaseModel
from langchain_core.messages import AIMessage
from langgraph.graph.message import add_messages
from typing import Literal, TypedDict
from operator import add


class RetieveSchema(BaseModel):
    query: str = Field(description="query to execute")
    state: Annotated[dict, InjectedState]
    tool_call_id: Annotated[str, InjectedToolCallId]


class RAGPipeline:
    def __init__(
        self,
        vectorstore: VectorStore,
        checkpoint: BaseCheckpointSaver,
        topic_guard_prompt: str,
        rag_system_prompt: str,
        llm_temperature: float = 0.1,
        llm_model_name: str = "gpt-4o-mini",
        num_history_messages: int = 5,
        num_retrieval_chunks: int = 3,
    ):
        assert os.getenv(
            "OPENAI_API_KEY"
        ), "OPENAI_API_KEY not found in environment variables"

        self.llm = ChatOpenAI(
            model_name=llm_model_name,
            temperature=llm_temperature,
        )

        self.trimmer = trim_messages(
            # in this case we want to keep the last messages
            max_tokens=num_history_messages,
            strategy="last",
            token_counter=len,
            include_system=True,
            start_on="human",
            end_on=("human", "tool"),
        )

        self.vectorstore = vectorstore
        self.topic_guard_prompt = topic_guard_prompt
        self.rag_system_prompt = rag_system_prompt
        self.llm_temperature = llm_temperature
        self.llm_model_name = llm_model_name
        self.num_history_messages = num_history_messages
        self.num_retrieval_chunks = num_retrieval_chunks
        self.checkpoint = checkpoint
        self.graph = self._setup_graph()

    def _create_retrieval_tool(self) -> StructuredTool:
        """Create the retrieval tool to use in the LLM"""

        @limit_calls(max_calls=6)
        def retrieve(
            query: str,
            state: Annotated[dict, InjectedState],
            tool_call_id: Annotated[str, InjectedToolCallId],
        ):
            """Retrieve information related to a query."""
            retrieved_docs = self.vectorstore.similarity_search(
                query=query,
                k=self.num_retrieval_chunks,
            )
            content = "\n\n".join([doc.page_content for doc in retrieved_docs])

            # TODO: use the real metadata fields
            references = list(
                {
                    doc.metadata.get("source")
                    for doc in retrieved_docs
                    if doc.metadata.get("source")
                }
            )
            return Command(
                update={
                    "references": references,
                    "messages": [
                        ToolMessage(content=content, tool_call_id=tool_call_id)
                    ],
                }
            )

        retrieve_tool = StructuredTool(
            description="Retrieve information related to a query.",
            name="retrieve_tool",
            func=retrieve,
            args_schema=RetieveSchema,
        )

        return retrieve_tool

    def _setup_graph(self) -> CompiledStateGraph:
        """Setup the graph for the chatbot"""

        tools = [
            self._create_retrieval_tool(),
        ]
        model_with_tools = self.llm.bind_tools(tools)

        class State(TypedDict):
            """Define the state schema for the workflow in the graph."""

            messages: Annotated[list, add_messages]
            references: Annotated[list, add]
            num_calls: Annotated[list, add]

        graph_builder = StateGraph(State)

        def topic_guard(state: State) -> Command[Literal["LLM_with_retriever", END]]:
            """Entry point of the workflow in charge of checking if the topic
            is related to the content and cleaning the tool messages and
            references used previously.
            """

            class TopicGuardOutput(BaseModel):
                related_topic: bool = Field(
                    description="when the topic is related to the content"
                )
                answer: str | None = Field(
                    description="The polite answer to the user when the topic is not related to the content or a comment about why the topic is related to the content"
                )

            state["references"].clear()  # reset references
            state["num_calls"].clear()  # reset num_calls

            # no need to include tool messages used previously
            conversation_messages = [
                message
                for message in state["messages"]
                if message.type in ("human", "system")
                or (message.type == "ai" and not message.tool_calls)
            ]
            # keep only the conversation messages
            state["messages"].clear()
            state["messages"].extend(conversation_messages)

            trimmed_messages = self.trimmer.invoke(state["messages"])

            output: TopicGuardOutput = self.llm.with_structured_output(
                TopicGuardOutput
            ).invoke(
                [SystemMessage(content=self.topic_guard_prompt)] + trimmed_messages
            )

            if output.related_topic:
                return Command(
                    goto="LLM_with_retriever",
                )
            else:
                return Command(
                    goto=END,
                    update={
                        "messages": [AIMessage(content=output.answer)],
                        "references": [],
                        "num_calls": [],
                    },
                )

        def llm_with_retriever(state: State):
            # find the last message of type human
            last_human_message = 0
            for i, message in enumerate(state["messages"]):
                if message.type == "human":
                    last_human_message = i + 1  # to include the last user message

            # We don't want to trim the tool messages used previously
            trimmed_messages = self.trimmer.invoke(
                state["messages"][:last_human_message]
            )

            # add the tool messages used previously
            trimmed_messages.extend(state["messages"][last_human_message:])
            return {
                "messages": [
                    model_with_tools.invoke(
                        [SystemMessage(content=self.rag_system_prompt)]
                        + trimmed_messages  # conversation messages
                    )
                ]
            }

        graph_builder.add_node("Topic_guard", topic_guard)
        graph_builder.add_node("LLM_with_retriever", llm_with_retriever)

        tool_node = ToolNode(tools=tools, name="DB_retriever")
        graph_builder.add_node("DB_retriever", tool_node)

        graph_builder.add_conditional_edges(
            "LLM_with_retriever",
            tools_condition,
            {"tools": "DB_retriever", END: END},
        )

        graph_builder.add_edge("DB_retriever", "LLM_with_retriever")
        graph_builder.add_edge(START, "Topic_guard")

        graph = graph_builder.compile(checkpointer=self.checkpoint)

        return graph

    def chat(
        self, user_input: str, config={"configurable": {"thread_id": "1"}}
    ) -> tuple[str, list[str]]:
        output = self.graph.invoke({"messages": [("user", user_input)]}, config)

        return output["messages"][-1].content, output["references"]
