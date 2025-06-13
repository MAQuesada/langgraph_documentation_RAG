from functools import lru_cache
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore

from pathlib import Path
from langchain_openai import OpenAIEmbeddings


EMBED_MODEL = "text-embedding-3-large"
DIMENSION = 1024
QDRANT_PATH = Path("qdrant_data")
COLLECTION_NAME = "langgraph_docs"
EMBEDDINGS_DIR = Path("docs/embeddings")
EMBEDDINGS_FILE = EMBEDDINGS_DIR / "embeddings.npy"
METADATA_FILE = EMBEDDINGS_DIR / "chunk_metadata.json"


@lru_cache(maxsize=1)
def get_vector_store() -> QdrantVectorStore:
    """
    Initializes and returns a Qdrant vector store instance.
    This function uses caching to ensure that the vector store is only created once.
    """
    client = QdrantClient(path=str(QDRANT_PATH))
    embeddings = OpenAIEmbeddings(model=EMBED_MODEL, dimensions=DIMENSION)
    if COLLECTION_NAME not in [
        col.name for col in client.get_collections().collections
    ]:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=DIMENSION, distance=Distance.COSINE),
        )
    vector_store = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings,
    )
    return vector_store
