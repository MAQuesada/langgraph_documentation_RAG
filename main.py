from vector_database.src.documentation_loader import (
    load_config, clone_repo, cleanup_old_outputs, load_documents
)
from vector_database.src.text_splitter import chunk_documents, save_chunks_to_disk
from vector_database.src.vector_store import store_embeddings
from vector_database.src.utils import load_config
from dotenv import load_dotenv
from pathlib import Path

def main():
    load_dotenv()

    config_path = Path(__file__).parent/"config.yaml"

    config = load_config(config_path)

    cleanup_old_outputs()

    clone_repo(config)

    docs_path = config['data_source']['github']['target_path']
    all_docs = load_documents(docs_path)

    chunks = chunk_documents(all_docs, config)
    save_chunks_to_disk(chunks)

    store_embeddings(chunks, config)


if __name__ == "__main__":
    main()
