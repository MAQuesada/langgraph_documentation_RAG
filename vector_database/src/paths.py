from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = ROOT_DIR / ".env"
CONFIG_PATH = ROOT_DIR / "vector_database" / "src" / "config.yaml"
PARSED_DOCS_PATH = ROOT_DIR / "vector_database" / "processed_docs"
PARSED_DOCS_PATH.mkdir(parents=True, exist_ok=True)
