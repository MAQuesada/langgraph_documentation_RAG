from git import Repo, GitCommandError
import os
import stat
import shutil
from mrkdwn_analysis import MarkdownAnalyzer
from pathlib import Path
from vector_database.src.utils import load_config  


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




def parse_markdown_and_codeblocks(docs_root, output_dir):
    docs_root = Path(docs_root)
    output_dir = Path(output_dir)
    code_dir = output_dir / "code_blocks"
    text_dir = output_dir / "text_blocks"
    code_dir.mkdir(parents=True, exist_ok=True)
    text_dir.mkdir(parents=True, exist_ok=True)

    for file_path in docs_root.rglob("*.md"):
        analyzer = MarkdownAnalyzer(str(file_path))
        code_blocks = analyzer.identify_code_blocks().get("Code block", [])
        paragraphs = analyzer.identify_paragraphs().get("Paragraph", [])

        # Use stem to avoid extension, add hash if needed for uniqueness
        code_out = code_dir / f"{file_path.stem}_codeblocks.txt"
        text_out = text_dir / f"{file_path.stem}_text.txt"

        with open(code_out, "w", encoding="utf-8") as cb_out:
            for block in code_blocks:
                cb_out.write(f"Language: {block.get('language', 'unknown')}\n")
                cb_out.write(block["content"])
                cb_out.write("\n\n---\n\n")
        with open(text_out, "w", encoding="utf-8") as txt_out:
            for para in paragraphs:
                txt_out.write(para + "\n\n")

     
    print(f"\nCode block files in {code_dir}:")
    for f in code_dir.iterdir():
        print(f.name)
    print(f"\nText block files in {text_dir}:")
    for f in text_dir.iterdir():
        print(f.name)

    

if __name__ == "__main__":
    

    config = load_config()
    clone_repo(config)
    
    docs_path = config["data_source"]["github"]["target_path"]
    parse_markdown_and_codeblocks(docs_root=docs_path, output_dir="outputs/parsed_docs")