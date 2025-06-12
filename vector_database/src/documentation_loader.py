from git import Repo, GitCommandError
import os
import stat
import shutil
from pathlib import Path
from langchain_core.documents import Document


def handle_remove_readonly(func, path, exc):
    """Handle read-only files during directory removal."""
    os.chmod(path, stat.S_IWRITE)  # Make file writable
    func(path)  # Retry the operation


def clone_repo(config: dict):
    """Clones a GitHub repo copies it from a local cache, depending on the config.

    Args:
        config (dict) : Configuration dictionary loaded from config.yaml"""

    github_config = config["data_source"]["github"]
    clone_url = github_config["clone_url"]
    target_path = github_config["target_path"]
    local_cache = github_config.get("local_cache", None)

    target_path = os.path.abspath(target_path)

    if os.path.exists(target_path):
        print(f"Target path {target_path} already exists. Removing for fresh clone.")

        shutil.rmtree(target_path, onerror=handle_remove_readonly)

    if local_cache and os.path.exists(local_cache):
        print(f"Copying from local cache {local_cache} to {target_path}...")
        shutil.copytree(local_cache, target_path)

    else:
        print(f"Cloning from {clone_url} to {target_path}...")
        try:
            Repo.clone_from(clone_url, target_path)
        except GitCommandError as e:
            print(f"Error cloning repository : {e}")

    if not os.listdir(target_path):
        raise ValueError(f"Cloned/copied directory {target_path} is empty!")


def cleanup_old_outputs(file_path="outputs/source_docs"):
    """Removes the old outputs directory if it exists."""

    base_output = Path(file_path)
    if base_output.exists():
        print(f"Removing old directory : {base_output}")
        shutil.rmtree(base_output)


def load_documents(docs_root: str, extensions=(".md", ".ipynb")) -> list[Document]:
    """Loads documents from a directory."""

    docs = []
    root = Path(docs_root)

    for path in root.rglob("*"):
        if path.is_file() and path.suffix in extensions:
            with open(path, encoding="utf-8") as f:
                content = f.read()
            docs.append(
                Document(
                    page_content=content,
                    metadata={"file_path": str(path), "file_type": path.suffix},
                )
            )
    return docs
