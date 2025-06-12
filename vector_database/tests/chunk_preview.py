from vector_database.src.documentation_loader import (
    clone_repo,
    cleanup_old_outputs,
    load_documents,
)
from vector_database.src.text_splitter import chunk_documents, save_chunks_to_disk
from dotenv import load_dotenv

from vector_database.src.utils import load_config

load_dotenv()


def preview_chunks(chunks, limit=3):
    for i, chunk in enumerate(chunks[:limit]):
        print(f"\n--- Chunk {i+1} ---")
        print("Metadata:", chunk.metadata)
        # first 500 chars
        print("Content Preview:\n", chunk.page_content[:500])


if __name__ == "__main__":
    cleanup_old_outputs()
    config = load_config()
    clone_repo(config)
    docs_path = config["data_source"]["github"]["target_path"]

    all_docs = load_documents(docs_path)
    chunks = chunk_documents(all_docs, config)
    save_chunks_to_disk(chunks)

    preview_chunks(chunks, limit=5)
