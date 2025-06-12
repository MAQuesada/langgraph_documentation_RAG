from typing import List
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from pathlib import Path
import json


load_dotenv()


def chunk_documents(documents: list[Document], config: dict) -> List[Document]:
    """Chunks documents into smaller segments."""

    chunking_config = config["document_processing"]["chunking"]
    chunk_size = chunking_config.get("chunk_size", 5000)
    chunk_overlap = chunking_config.get("chunk_overlap", 600)

    all_chunks = []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )

    filtered_docs = [
        doc
        for doc in documents
        if doc is not None
        and (
            (isinstance(doc, dict) and "page_content" in doc)
            or hasattr(doc, "page_content")
        )
    ]

    for doc in filtered_docs:
        metadata = {
            "source": doc.metadata.get("file_path", "unknown"),
            "file_type": doc.metadata.get("file_type", "unknown"),
        }
        try:
            content = doc["page_content"] if isinstance(doc, dict) else doc.page_content
            metadata = (
                doc["metadata"]
                if isinstance(doc, dict)
                else getattr(doc, "metadata", {})
            )

            final_chunks = splitter.split_documents(
                [Document(page_content=content, metadata=metadata)]
            )
            all_chunks.extend(final_chunks)

        except Exception as e:
            file_path = metadata.get("file_path", "unknown") if metadata else "unknown"
            print(f"Chunking failed for {file_path} = {e}")

    return all_chunks


def save_chunks_to_disk(
    chunks: list[Document], output_dir: str = "docs/chunked_docs"
) -> None:
    """Saves chunks of documents to disk."""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    chunks_data = []
    for i, chunk in enumerate(chunks):
        chunks_data.append(
            {"id": i, "content": chunk.page_content, "metadata": chunk.metadata}
        )

    with open(output_path / "chunked_docs.json", "w", encoding="utf-8") as f:
        json.dump(chunks_data, f, indent=2, ensure_ascii=False)

    print(f"\n Saved {len(chunks)} chunks to {output_path/'chunked_docs.json'}")
