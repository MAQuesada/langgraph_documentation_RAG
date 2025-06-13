# LangGraph RAG Agent: Retrieval-Augmented Generation over Technical Documentation

## 📌 Abstract

Retrieval-Augmented Generation (RAG) has emerged as a powerful framework for building LLM-based assistants that can access dynamic external knowledge without retraining. In this project, we develop a LangGraph-powered RAG system capable of answering complex technical questions by retrieving and reasoning over the official LangGraph documentation. Our architecture integrates LangChain, Qdrant vector store, and OpenAI's `text-embedding-3-large`, delivering a modular and scalable assistant that understands and explains multi-agent workflows in LangGraph. The project demonstrates how a LangGraph-based agent can be constructed to interact with domain-specific content with contextual memory, prompt modularity, and strong reasoning capabilities.

---

## 🔍 Introduction

Large Language Models (LLMs) often struggle to answer niche or domain-specific queries unless fine-tuned on custom data—an expensive and time-consuming process. RAG solves this by combining LLMs with an external retrieval mechanism, allowing real-time access to updated content while minimizing computational costs.

This project leverages:

- **LangGraph**: for defining the agent workflow and state transitions.
- **LangChain**: for LLM abstraction and orchestration.
- **Qdrant**: as a scalable vector database.
- **OpenAI**: for embeddings and language generation.

The target use case is to assist users in exploring LangGraph’s complex features and documentation through natural language queries—answering everything from architectural concepts to agent behavior.

---

## 🏗️ System Architecture

![System Architecture](docs/architecture.png)

### 📚 Document Ingestion

LangGraph documentation is cloned from its public repository using a custom ingestion pipeline (`main.py`, `vector_database/src/`). The process includes:

- Cleaning old outputs
- Loading all markdown and text files
- Recursive chunking (1000–2000 tokens)
- Saving processed chunks for embedding

**Document Stats:**

- Total documents: 184
- Min length: 264, Max: 88,210
- Avg length: 10,370, Median: 7,471

Chunks are embedded using OpenAI’s `text-embedding-3-large` and indexed into Qdrant with metadata.

---

### 🧠 Prompting Strategy

Prompt templates are defined in structured YAML files under `prompts/` and modularized via a Python class. Supported reasoning styles include:

- **ReAct (Retrieve-Act)**
- **Chain-of-thought**
- **Self-ask**

#### Prompt Components

- **System Prompt**: Filters irrelevant queries.
- **Chatbot Prompt**: Drives retrieval and reasoning, decomposes questions if needed, and guides GPT-4 response generation.

---

### 🔎 Vector Store (Qdrant)

Qdrant is used for storing and retrieving document chunks. Key reasons for selection:

- Efficient similarity search with REST API
- Metadata-based filtering support
- Easy local deployment

Search is based on cosine similarity over OpenAI embeddings.

---

### 🤖 RAG Pipeline with LangGraph

LangGraph powers the structured logic of the agent:

- **Each user query** becomes a new LangGraph workflow.
- Nodes represent tools: retriever, prompt executor, memory.
- **Retriever Node** queries Qdrant for relevant chunks.
- **LLM Node** decides to:
  - Answer directly
  - Fetch more info via sub-questions
  - Store interaction in memory (5-turn limit)
- LangGraph manages the flow and context through each turn.

---

### 💬 Memory and Context Handling

LangGraph’s native memory (e.g., checkpointing with PostgreSQL) enables:

- Persistent session context
- Multi-turn dialogue coherence (trimmed to 5 interactions)
- Session recovery

---

## 💻 Example Use Cases

> “What is the difference between a workflow and an agent in LangGraph?”
> → Two tool calls retrieve definitions, which are then synthesized into an answer.

> “How does checkpointing work in LangGraph?”
> → Retrieves from memory documentation and explains usage.

> “Explain how multi-agent routing is handled in LangGraph.”
> → Pulls and compares relevant docs to generate a guided summary.

---

## ✅ Observations

### 💪 Strengths

- Modular, scalable RAG implementation
- Handles deep technical queries (multi-hop reasoning)
- Built on open, production-ready tools

### ⚠️ Limitations

- Chunking quality heavily impacts retrieval performance
- Latency can increase with decomposition/retrieval loops
- No reranking or cross-encoder scoring used yet

---

## 🧩 Conclusion

This project showcases LangGraph’s utility not only as an orchestration engine but as a knowledge domain itself. The RAG system allows for intuitive exploration of technical concepts, enabling precise responses grounded in source documentation.

---

## 🚀 Future Work

- Integrate reranking using LLM or cross-encoder
- Summarize long documents before indexing
- Add user personalization in memory and retrieval paths

---

## 👥 Contributors

- **Manuel** – LangGraph workflow + RAG Agent
- **Utkarsh** – Vector DB ingestion and embeddings
- **Pranav** – Research, system documentation, and publication

---

## 📫 Contact 
Open to collaboration and contributions:

-📧 Email: [mailto:tu_email@ejemplo.com, tiwari.pranav1999@gmail.com, utkarsh251096@gmail.com]
-🌐 GitHub: [tu\_usuario](https://github.com/tu_usuario)

