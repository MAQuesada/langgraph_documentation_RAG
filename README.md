# LangGraph Documentation RAG 🤖🚀

...<description here>...

## Dependencies Management with Poetry

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

## Pre-commit Setup

Once you have installed the dependencies using `poetry install`, you will need to configure pre-commit hooks:

```python
pre-commit install
```

This command sets up the pre-commit hooks that automatically format your code according to the rules defined in the `.pre-commit-config.yaml` file. The hooks are executed before each commit, and if any rule fails, the commit will be blocked. You can also run the hooks manually with:

```python
pre-commit run --all
```

<!-- ___

##  Docker Development Setup

Follow these steps to get the main application running using Docker:

1. **Ensure Prerequisites Are Installed**
   Verify that Docker and Docker Compose are installed:
   ```bash
   docker --version
   docker-compose --version
   ```

2. **Configure Environment Variables**
   Create a `.env` file in the project root with the required environment variables (e.g., API keys, tokens).

3. **Build and Start the Container**
   Run the following command to build the Docker image and start the container:
   ```bash
   docker-compose up --build -d
   ```
   > **Note:** The `--build` flag forces a rebuild of the Docker image. This ensures that any changes to the source code, dependencies, or configurations are incorporated into the container.

4. **Monitor the Application**
   Check the logs to verify that the application is running properly:
   ```bash
   docker-compose logs -f
   ```

5. **Development Workflow**
   Since the project’s source code is mounted as a volume, changes made locally will be reflected immediately in the running container. If you update dependencies or configuration files, remember to run `docker-compose up --build` again to rebuild the image and apply these changes.
``` -->
