
# 🤖 LangGraph Documentation RAG Assistant

A **Retrieval-Augmented Generation (RAG)** agent designed to answer technical questions from the **LangGraph documentation** using its own text corpus. This project integrates **LangGraph** workflows, **LangChain**, **Qdrant** vector database, and **OpenAI** embeddings + GPT-4 to build a fully functional domain-specific assistant.

---


## 🧠 Architecture Overview


![flows](https://github.com/user-attachments/assets/5b901790-8753-47fb-be2c-f06aa0590f49)


---

## ⚙️ Tech Stack

| Component        | Tool / Service              | Purpose                           |
|------------------|-----------------------------|-----------------------------------|
| **LLM**          | OpenAI GPT-4                | Response generation               |
| **Embeddings**   | `text-embedding-3-large`    | Document vectorization            |
| **Agent Logic**  | LangGraph                   | Agent and tool-based workflow     |
| **Vector DB**    | Qdrant                      | Document chunk retrieval          |
| **Prompting**    | LangChain                   | Modular prompt orchestration      |
| **Environment**  | Poetry                      | Dependency & virtual env setup    |

---

## 🚀 Features

- 📚 Uses official LangGraph documentation as source
- 🔍 Semantic search via Qdrant
- 🧠 Modular prompts with ReAct-style reasoning
- 🔄 LangGraph-driven state-based retrieval and generation
- 💬 Supports multi-turn memory (within LangGraph state)

---

## 📂 Project Structure

```
.
├── main.py                       # Runs document ingestion pipeline
├── publication.md               # Technical write-up
├── prompts/                     # YAML-based prompt templates
├── rag_pipeline/                # Core agent orchestration
├── test_notebooks/             # Prompt testing and demo notebooks
├── vector_database/            # Qdrant vector store integration
├── example.env                  # Sample environment config
├── config.yaml                  # Global config for chunking, DB, etc.
├── README.md                    # You’re reading it :)
└── docs/
    └── architecture.png         # 🖼️ Place your diagram here
```

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/langgraph_documentation_RAG
cd langgraph_documentation_RAG
```

### 2. Install Dependencies with Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
poetry install
poetry shell
```

### 3. Set Up Environment Variables

Create a `.env` file using the sample provided:

```bash
cp example.env .env
```

Then update your `.env` with your OpenAI API key:

```
OPENAI_API_KEY=your-key-here
```

---

## 🧪 Run the Ingestion Pipeline

```bash
poetry run python main.py
```

This will:
- Clone LangGraph documentation repo
- Load and chunk files
- Store vectorized content into Qdrant

---

## 📓 Example Notebooks

Test and interact with the assistant in the following Jupyter notebooks:

- `test_notebooks/rag_example.ipynb`
- `test_notebooks/prompt_template_example.ipynb`

---

## 💡 Example Queries

```text
“What is the difference between a LangGraph workflow and an agent?”

“How can I use checkpoints or memory between steps in LangGraph?”

“Explain multi-agent routing with LangGraph.”
```

---

## 🔖 License

This project is open source and available under the **MIT License**.

---

## 👥 Contributors

- **Pranav Tiwari** – Research + Publication  
- **Utkarsh** – Vector DB Engineering  
- **Manuel** – LangGraph Agent Implementation

---

## 📫 Contact Open to collaboration and contributions: 
📧 Email: [mailto:tu_email@ejemplo.com, tiwari.pranav1999@gmail.com, utkarsh251096@gmail.com] 
🌐 GitHub: tu_usuario
