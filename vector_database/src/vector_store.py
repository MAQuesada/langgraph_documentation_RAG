from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from pathlib import Path
import uuid
import json
import numpy as np
import os

EMBED_MODEL = 'all-MiniLM-L6-v2'
QDRANT_PATH = Path('qdrant_data')
COLLECTION_NAME = 'langgraph_docs'
EMBEDDINGS_DIR = Path("docs/embeddings")
EMBEDDINGS_FILE = EMBEDDINGS_DIR / "embeddings.npy"
METADATA_FILE = EMBEDDINGS_DIR / "chunk_metadata.json"

embedder = SentenceTransformer(EMBED_MODEL)
client = QdrantClient(path=str(QDRANT_PATH))

def store_embeddings(chunks, config=None):
    # Ensure collection exists
    if COLLECTION_NAME not in [col.name for col in client.get_collections().collections]:
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )

    # Load from disk if embeddings exist
    if EMBEDDINGS_FILE.exists() and METADATA_FILE.exists():
        print("🔁 Loading precomputed embeddings from disk...")
        embeddings = np.load(EMBEDDINGS_FILE)

        with open(METADATA_FILE, encoding="utf-8") as f:
            metadata_list = json.load(f)
    else:
        print(f"Generating embeddings for {len(chunks)} chunks...")
        texts = [chunk.page_content for chunk in chunks]
        embeddings = embedder.encode(texts, convert_to_numpy=True)

        # Save to disk for reuse
        EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)
        np.save(EMBEDDINGS_FILE, embeddings)

        with open(METADATA_FILE, "w", encoding="utf-8") as f:
            json.dump([chunk.metadata for chunk in chunks], f, indent=2)

        metadata_list = [chunk.metadata for chunk in chunks]

    # Upload to Qdrant
    print("Uploading embeddings to Qdrant...")
    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=embeddings[i],
            payload=metadata_list[i]
        )
        for i in range(len(metadata_list))
    ]

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"✅ Uploaded {len(points)} embeddings to collection '{COLLECTION_NAME}'")


def search_qdrant(query: str, top_k: int = 5):
    query_vector = embedder.encode(query, convert_to_numpy=True)

    search_result = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True
    )

    print(f"\nTop {top_k} results for query: '{query}'\n")
    for i, hit in enumerate(search_result):
        content = hit.payload.get("source", "No source info")
        print(f"{i+1}. Score: {hit.score:.4f} | Source: {content}")
        print(f"   Metadata: {hit.payload}")
        print()
