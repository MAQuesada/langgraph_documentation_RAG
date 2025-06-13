# 🧠 LangGraph Documentation RAG Assistant

A Retrieval-Augmented Generation (RAG) agent built with **LangGraph**, capable of answering technical questions about the LangGraph framework using its own documentation as the knowledge base.

This project demonstrates a full-stack implementation of a **domain-specific assistant**, integrating document parsing, chunking, embedding, vector search, agent reasoning, memory handling, and monitoring — all using modern LLM tooling.

---

## 🔧 Tech Stack

| Component        | Tool/Service              | Purpose                             |
|------------------|---------------------------|-------------------------------------|
| **LLM**          | OpenAI (GPT-4)            | Language generation                 |
| **Embeddings**   | `text-embedding-3-large`  | Document vectorization              |
| **Vector DB**    | Qdrant                    | Semantic retrieval                  |
| **Agent Engine** | LangGraph                 | Workflow orchestration              |
| **LLM Orchestration** | LangChain            | Tool chaining and prompts           |
| **Monitoring**   | LangSmith                 | Observability and traceability      |
| **Memory**       | PostgreSQL (LangGraph)    | Multi-turn memory checkpointing     |
| **Environment**  | Poetry                    | Dependency and environment management

---

## 🧩 Features

- ✅ RAG pipeline with real-time semantic search over LangGraph docs
- 🧠 Modular prompt design using ReAct and chain-of-thought
- 🗃️ Efficient document chunking + embedding via OpenAI
- 💬 Memory-augmented conversations (5-turn limit)
- 📊 Evaluation and traceability via LangSmith
- 📂 Configurable YAML-based workflows

---

## 📁 Project Structure
langgraph_documentation_RAG/
├── main.py # Document ingestion and chunking
├── vector_database/ # Vector indexing pipeline
│ ├── src/
│ │ ├── documentation_loader.py
│ │ ├── text_splitter.py
│ │ └── utils.py
├── config.yaml # RAG + ingestion configuration
├── prompts/ # Prompt templates in YAML
├── publication.md # Formal technical documentation
├── README.md # Project guide
└── .env # API keys & environment variables



---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/MAQuesada/langgraph_documentation_RAG
cd langgraph_documentation_RAG


### 2. Install Dependencies (Using Poetry)
Make sure Poetry is installed:
curl -sSL https://install.python-poetry.org | python3 -

•Install dependencies:

poetry install

poetry shell

### 3. Set Environment Variables
Create a .env file with your OpenAI API key and other credentials:
OPENAI_API_KEY=your-api-key

🛠️ Run the Pipeline
Step 1: Preprocess Documents
bash
poetry run python main.py

This will:
•Clone the LangGraph documentation repo

•Split and chunk content

•Prepare documents for vector embedding

Step 2: Launch the Assistant (Jupyter/Streamlit/Notebook)
You can now start querying the agent inside a notebook or terminal interface. Add LangGraph workflows that use retriever + prompt components to complete the full pipeline.

💬 Example Queries
•“What is the difference between a router and a supervisor in LangGraph?”

•“How does LangGraph handle memory between agent steps?”

•“Can you explain how tool calling is implemented in LangGraph?”

🧪 Monitoring with LangSmith
Enable LangSmith in your .env and use it to:

•Trace tool usage and output

•Compare versions

•Debug LLM responses

🧾 Publication
For a formal explanation of the design, methods, and contributions, read our full 📄 publication.md

👥 Contributors
Pranav Tiwari — Research, Documentation, Publication

Utkarsh — Vector Database and Embedding System

Manuel — RAG Agent + LangGraph Workflow

📬 Contact & Contributions
We welcome pull requests, feedback, and collaboration!
📧 Email: [mailto:tu_email@ejemplo.com, tiwari.pranav1999@gmail.com, utkarsh251096@gmail.com]
🌐 GitHub: tu_usuario

📘 License
This project is open source under the MIT License.
