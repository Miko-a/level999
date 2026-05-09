import os
from pathlib import Path
from typing import List, Dict

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction


BASE_DIR = Path(__file__).resolve().parent.parent

VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH")

if VECTOR_DB_PATH:
    VECTOR_DB_DIR = Path(VECTOR_DB_PATH)
else:
    VECTOR_DB_DIR = BASE_DIR / "vector_db"

COLLECTION_NAME = "hsr_knowledge"
MIN_SIMILARITY_SCORE = 0.25

COLLECTION_NAME = "hsr_knowledge"

MIN_SIMILARITY_SCORE = 0.25

embedding_function = SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def get_chroma_client():
    return chromadb.PersistentClient(path=str(VECTOR_DB_DIR))


def get_or_create_collection():
    client = get_chroma_client()

    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function,
        metadata={
            "hnsw:space": "cosine"
        },
    )


def reset_collection():
    client = get_chroma_client()

    try:
        client.delete_collection(name=COLLECTION_NAME)
    except Exception:
        pass

    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function,
        metadata={
            "hnsw:space": "cosine"
        },
    )


def search_similar_chunks(query: str, top_k: int = 5) -> List[Dict]:
    collection = get_or_create_collection()

    result = collection.query(
        query_texts=[query],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]

    retrieved_chunks = []

    for index, document in enumerate(documents):
        metadata = metadatas[index]
        distance = distances[index]

        similarity_score = max(0.0, 1.0 - float(distance))

        if similarity_score < MIN_SIMILARITY_SCORE:
            continue

        retrieved_chunks.append(
            {
                "title": metadata.get("title", "Untitled"),
                "source_id": metadata.get("source_id", "unknown"),
                "file_name": metadata.get("file_name", "unknown"),
                "chunk_id": metadata.get("chunk_id", "unknown"),
                "category": metadata.get("category", "general"),
                "topic": metadata.get("topic", "unknown"),
                "version": metadata.get("version", "unknown"),
                "content": document,
                "score": round(similarity_score, 4),
                "preview": document[:300].replace("\n", " "),
            }
        )

    return retrieved_chunks


def build_context_from_chunks(chunks: List[Dict]) -> str:
    if not chunks:
        return ""

    context_parts = []

    for index, chunk in enumerate(chunks, start=1):
        context_parts.append(
            f"""
[Source {index}]
Title: {chunk["title"]}
Source ID: {chunk["source_id"]}
File: {chunk["file_name"]}
Chunk ID: {chunk["chunk_id"]}
Category: {chunk["category"]}
Topic: {chunk["topic"]}
Version: {chunk["version"]}
Similarity Score: {chunk["score"]}

Content:
{chunk["content"]}
"""
        )

    return "\n\n".join(context_parts)


def get_vector_stats() -> Dict:
    collection = get_or_create_collection()

    return {
        "collection_name": COLLECTION_NAME,
        "chunk_count": collection.count(),
    }