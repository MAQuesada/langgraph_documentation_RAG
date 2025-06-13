# LangGraph RAG Agent: Retrieval-Augmented Generation over Technical Documentation

## 📌 Abstract

Retrieval-Augmented Generation (RAG) has emerged as a powerful framework for building LLM-based assistants that can access dynamic external knowledge without retraining. In this project, we develop a LangGraph-powered RAG system capable of answering complex technical questions by retrieving and reasoning over the official LangGraph documentation. Our architecture integrates LangChain, Qdrant vector store, OpenAI's `text-embedding-3-large`, and LangSmith for monitoring, delivering a modular and scalable assistant that understands and explains multi-agent workflows in LangGraph. The project demonstrates how a LangGraph-based agent can be constructed to interact with domain-specific content with contextual memory, prompt modularity, and strong traceability.

---

## 🔍 Introduction

Large Language Models (LLMs) often struggle to answer niche or domain-specific queries unless fine-tuned on custom data—an expensive and time-consuming process. RAG solves this by combining LLMs with an external retrieval mechanism, allowing real-time access to updated content while minimizing computational costs.

This project leverages:
- **LangGraph**: for defining the agent workflow and state transitions.
- **LangChain**: for LLM abstraction and orchestration.
- **Qdrant**: as a scalable vector database.
- **OpenAI**: for embeddings and language generation.
- **LangSmith**: for performance monitoring and debugging.

The target use case is to assist users in exploring LangGraph’s complex features and documentation through natural language queries—answering everything from architectural concepts to agent behavior.

---

## 🏗️ System Architecture

### 1. 📚 Document Ingestion

LangGraph documentation is cloned from its public repository using a custom ingestion pipeline. The process includes:
- Cleaning old outputs
- Loading all markdown and text files
- Recursive chunking with a max chunk size (e.g., 1000–2000 tokens)
- Saving processed chunks for embedding

```bash
Total number of documents: 184
Chunk lengths: 
- Min: 264
- Max: 88,210
- Avg: 10,370
- Median (Q2): 7,471
These chunks are then embedded using OpenAI’s text-embedding-3-large model and indexed into Qdrant with appropriate metadata.

2. 🧠 Prompting Strategy
Prompt templates are defined using a YAML-driven structure and modularized via a custom Python class. We support reasoning strategies including:

ReAct (retrieve-act)

Chain-of-thought

Self-ask

Prompt Components:
System Prompt: Filters irrelevant queries and ensures the assistant responds only to LangGraph-related questions.

Chatbot Prompt: Guides the model through the retrieval and reasoning process, often breaking down a single query into multiple tool-based retrieval steps.

3. 🔎 Vector Store (Qdrant)
We chose Qdrant for its efficient similarity search, REST API, and production-readiness. Indexed chunks are embedded using OpenAI’s embedding model and stored with contextual metadata (title, section, file path). Search queries are performed using cosine similarity to fetch the top-k relevant chunks per user input.

4. 🤖 RAG Pipeline with LangGraph
LangGraph powers the logic of the agent’s interaction:

Each user query becomes a new workflow in LangGraph.

Nodes represent tool calls (retriever, prompt executor, memory manager).

The Retriever Node fetches context from Qdrant.

The LLM Node decides whether to:

Answer with current context

Ask sub-questions and fetch more info

Store conversation in memory (max 5 turns)

LangGraph also manages branching logic and agent state transitions with full traceability using LangSmith.

5. 💬 Memory and Context Handling
We integrate LangGraph’s native memory system using PostgreSQL checkpoints. This ensures:

Long-running conversations retain user context

State is restored across sessions

Trimming to 5 past interactions maintains focus and prevents bloating

🧪 Monitoring and Evaluation
We use LangSmith for:

Observing LLM inputs/outputs

Visualizing tool calls and retrieval paths

Measuring latency, response length, and accuracy

Conducting offline evaluation with saved traces

💻 Example Use Cases
“What is the difference between a workflow and an agent in LangGraph?”
→ The assistant breaks down the question into two tool calls, retrieves definitions from docs, and synthesizes a clear answer.

“How does checkpointing work in LangGraph?”
→ The assistant navigates to the memory documentation, retrieves steps, and formats a detailed guide.

“Explain how multi-agent routing is handled in LangGraph.”
→ The assistant fetches multiple docs, compares routing strategies, and provides examples from the codebase.

✅ Observations
✅ Strengths
Modular and well-structured RAG implementation

Agent can handle multi-hop technical queries

Stack uses only open-source components and scalable tools

⚠️ Limitations
Retrieval depends heavily on chunking quality

Latency increases with decomposition and multi-hop retrieval

Lacks reranking or cross-encoder scoring for better chunk selection

🧩 Conclusion
This project demonstrates the power of LangGraph as both a framework and knowledge source in building domain-specific RAG agents. The assistant provides reliable, traceable, and explainable responses on technical documentation—paving the way for customizable support agents across any domain.

🚀 Future Work
Integrate reranking via LLM or cross-encoder

Summarize long documents pre-indexing

Add user personalization to memory and retrieval

👥 Contributors
Manuel – LangGraph workflow + RAG Agent

Utkarsh – Vector DB ingestion and embeddings

Pranav – Research, system documentation, and publication

📫 Contact
Open to collaboration and contributions:
📧 Email: [[tu\_email@ejemplo.com](mailto:tu_email@ejemplo.com), tiwari.pranav1999@gmail.com,]
🌐 GitHub: [tu\_usuario](https://github.com/tu_usuario)

