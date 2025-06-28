
# 🤖 LangGraph Documentation RAG Assistant

A **Retrieval-Augmented Generation (RAG)** workflow designed to answer technical questions from the **LangGraph documentation** using its own text corpus. This project integrates **LangGraph** workflows, **LangChain**, **Qdrant** vector database, and **OpenAI** embeddings + GPT-4 to build a fully functional domain-specific assistant.

---

## 🧠 Architecture Overview

![2 excalidraw](https://github.com/user-attachments/assets/cc77e7f4-151b-4265-8ef1-e10e19db8359)

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
├── test_end_to_end.ipynb        # Chatbot execution end-to-end
├── publication.md               # Technical write-up
├── prompts/                     # YAML-based prompt templates
├── rag_pipeline/                # Core agent orchestration
├── test_notebooks/              # Prompt testing and demo notebooks
├── vector_database/             # Qdrant vector store integration
├── example.env                  # Sample environment config
├── config.yaml                  # Global config for chunking, DB, etc.
├── README.md                    # You’re reading it :)
└── docs/                        # Official LangGraph Documentation
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

## ▶️ Run the RAG Pipeline

Run the `test_end_to_end.ipynb` notebook. It will include:

- Clone the official LangGraph documentation repository.
- Load and split the documentation into optimized chunks.
- Generate embeddings using OpenAI’s text-embedding-3-large model.
- Store the embedded chunks into Qdrant for later retrieval.
- Build the RAG-pipeline instance.
- Create an interactive cell for chat.

### Example Queries

```text
“What is the difference between a LangGraph workflow and an agent?”

“How can I use checkpoints or memory between steps in LangGraph?”

“Explain multi-agent routing with LangGraph.”
```

---

## 🛠  For development

This project uses **Poetry** to manage dependencies and virtual environments efficiently.

### 1. Install Poetry

Ensure you have Poetry installed:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Verify the installation:

```bash
poetry --version
```

### 2. Initialize Poetry in the Project (First-Time Setup Only)

If this is the first time setting up the project, navigate to the project folder and initialize Poetry:

```bash
cd langgraph_documentation_RAG
poetry init
```

If the project is already initialized, skip this step and proceed to dependency installation.

### 3. Install Dependencies

Add the new dependencies to the project, for example:

```bash
poetry add numpy pandas requests
```

For development dependencies, use the following:

```bash
poetry add --dev black pytest
```

### 4. Activate the Virtual Environment

Poetry automatically creates a virtual environment. To activate it, first make sure to have installed :

```bash
poetry self add poetry-plugin-shell
```

Then, activate the virtual environment:

```bash
poetry shell
```

To run a script within the virtual environment without activating it:

```bash
poetry run python main.py
```

### 5. Store Virtual Environment in the Project (Optional)

To keep the virtual environment inside the project folder:

```bash
poetry config virtualenvs.in-project true
poetry install
```

This will create a `.venv/` directory inside the project.

### 6. Check the Environment Status

To view environment details:

```bash
poetry env info
```

To list installed dependencies:

```bash
poetry show
```

### 7. Reproducing the Environment on Another Machine

When cloning the project, run:

```bash
poetry install
```

This will install all dependencies as specified in `pyproject.toml` and `poetry.lock`.

### 8. Generating the requirements.txt using Poetry

Make sure the poetry-plugin-export plugin is installed. If not, you can install it with the following command:
 `poetry self add poetry-plugin-export`.

Then, export your project’s dependencies to a requirements.txt file using:

```bash
poetry export --without-hashes -f requirements.txt --output requirements.txt
```

### 9. Pre-commit Setup

Once you have installed the dependencies using `poetry install`, you will need to configure pre-commit hooks:

```python
pre-commit install
```

This command sets up the pre-commit hooks that automatically format your code according to the rules defined in the `.pre-commit-config.yaml` file. The hooks are executed before each commit, and if any rule fails, the commit will be blocked. You can also run the hooks manually with:

```python
pre-commit run --all
```

---

## 🔍 More details about this repository

- Ready Tensor Publication: [Stop Searching, Start Asking: LangGraph Documentation at Your Fingertips 🤖🚀](https://app.readytensor.ai/publications/stop-searching-start-asking-langgraph-docs-at-your-fingertips-H2rbE1JDof4y)

---

## 🔖 License

This project is open source and available under the **MIT License**.

---

## 👥 Contributors

- **Manuel** – LangGraph Agent Implementation
- **Utkarsh** – Vector DB Engineering
- **Pranav Tiwari** – Research + Publication

---

## 📫 Contact Open to collaboration and contributions

- 📧 **Email**:[ [malejandroquesada@gmail.com](mailto:malejandroquesada@gmail.com), [tiwari.pranav1999@gmail.com](mailto:tiwari.pranav1999@gmail.com), [utkarsh251096@gmail.com](mailto:utkarsh251096@gmail.com)]
