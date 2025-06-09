from vector_database.src import document_loader, metadata_handler, text_splitter, vector_store
from utils import load_config
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    config = load_config("config.yaml")

    docs = document_loader.load_documents(config)
    enriched_docs = metadata_handler.enrich_documents(docs, config)
    chunks = text_splitter.chunk_documents(enriched_docs, config)
    vector_store.store(chunks, config)


if __name__ == "__main__":
    main()
    print("Vector database setup completed successfully.")