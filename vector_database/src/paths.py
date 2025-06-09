import os
from pathlib import Path

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV_PATH = os.path.join(ROOT_DIR, ".env")

CONFIG_PATH = os.path.join(ROOT_DIR, "vector_database", "src", "config.yaml")

PARSED_DOCS_PATH = os.path.join(ROOT_DIR, "vector_database", "fetched_documentation")

os.makedirs(PARSED_DOCS_PATH, exist_ok=True)


