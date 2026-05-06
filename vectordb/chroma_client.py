"""
ChromaDB client — all vector storage logic lives here.
Used only by the MCP server (separate process), not by the agent directly.
"""

import uuid
from datetime import datetime
import chromadb

_collection = None


def get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path="./chroma_data")
        _collection = client.get_or_create_collection(
            name="intelligence",
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def add_document(company_name: str, content: str, source: str) -> None:
    get_collection().add(
        documents=[content],
        metadatas=[{
            "company_name": company_name,
            "timestamp": datetime.utcnow().isoformat(),
            "source": source,
        }],
        ids=[str(uuid.uuid4())],
    )


def search_documents(query: str, company_name: str, n_results: int = 3) -> list[str]:
    collection = get_collection()
    total = collection.count()
    if total == 0:
        return []

    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, total),
        where={"company_name": company_name},
    )
    return results["documents"][0] if results["documents"] else []
