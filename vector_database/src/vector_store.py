from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from pathlib import Path
import uuid
import json
import numpy as np
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document


EMBED_MODEL = "text-embedding-3-large"
DIMENSION = 1024
QDRANT_PATH = Path("qdrant_data")
COLLECTION_NAME = "langgraph_docs"
EMBEDDINGS_DIR = Path("docs/embeddings")
EMBEDDINGS_FILE = EMBEDDINGS_DIR / "embeddings.npy"
METADATA_FILE = EMBEDDINGS_DIR / "chunk_metadata.json"


client = QdrantClient(path=str(QDRANT_PATH))
embeddings = OpenAIEmbeddings(model=EMBED_MODEL, dimensions=DIMENSION)


def store_embeddings(chunks: list[Document], config: dict = {}):
    # Ensure collection exists
    if COLLECTION_NAME not in [
        col.name for col in client.get_collections().collections
    ]:
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=DIMENSION, distance=Distance.COSINE),
        )

    # Load from disk if embeddings exist
    if EMBEDDINGS_FILE.exists() and METADATA_FILE.exists():
        print("🔁 Loading precomputed embeddings from disk...")
        embedding_vectors = np.load(EMBEDDINGS_FILE)

        with open(METADATA_FILE, encoding="utf-8") as f:
            metadata_list = json.load(f)
    else:
        print(f"Generating embeddings for {len(chunks)} chunks...")
        texts = [chunk.page_content for chunk in chunks]
        embedding_vectors = embeddings.embed_documents(texts)

        # Save to disk for reuse
        EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)
        np.save(EMBEDDINGS_FILE, embedding_vectors)

        with open(METADATA_FILE, "w", encoding="utf-8") as f:
            json.dump([chunk.metadata for chunk in chunks], f, indent=2)

        metadata_list = [chunk.metadata for chunk in chunks]

    # Upload to Qdrant
    print("Uploading embeddings to Qdrant...")
    points = [
        PointStruct(
            id=str(uuid.uuid4()), vector=embedding_vectors[i], payload=metadata_list[i]
        )
        for i in range(len(metadata_list))
    ]

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"✅ Uploaded {len(points)} embeddings to collection '{COLLECTION_NAME}'")


def search_qdrant(query: str, top_k: int = 5):
    query_vector = embeddings.embed_query(query)

    search_result = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True,
    )

    print(f"\nTop {top_k} results for query: '{query}'\n")
    for i, hit in enumerate(search_result):
        content = hit.payload.get("source", "No source info")
        print(f"{i+1}. Score: {hit.score:.4f} | Source: {content}")
        print(f"   Metadata: {hit.payload}")
        print()
