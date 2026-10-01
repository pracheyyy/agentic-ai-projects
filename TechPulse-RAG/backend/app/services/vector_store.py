import json
from pathlib import Path

import faiss
import numpy as np

from app.services.embedding_service import embed_documents, embed_query


BASE_DIR = Path(__file__).resolve().parents[2]
VECTOR_DIR = BASE_DIR / "data" / "vectorstore"
INDEX_FILE = VECTOR_DIR / "techpulse.index"
DOCS_FILE = VECTOR_DIR / "documents.json"


def build_vector_store(documents: list[dict]) -> dict:
    if not documents:
        raise ValueError("No documents available for indexing.")

    VECTOR_DIR.mkdir(parents=True, exist_ok=True)

    texts = [
        f"{doc.get('title', '')}. {doc.get('summary', '')}"
        for doc in documents
    ]

    embeddings = np.asarray(
        embed_documents(texts),
        dtype="float32",
    )

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, str(INDEX_FILE))

    DOCS_FILE.write_text(
        json.dumps(documents, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return {
        "status": "success",
        "documents": len(documents),
        "embedding_dimension": int(embeddings.shape[1]),
        "knowledge_documents": sum(d.get("type") == "knowledge" for d in documents),
        "news_documents": sum(d.get("type") == "news" for d in documents),
    }


def load_vector_store():
    if not INDEX_FILE.exists() or not DOCS_FILE.exists():
        return None, []

    index = faiss.read_index(str(INDEX_FILE))
    documents = json.loads(DOCS_FILE.read_text(encoding="utf-8"))

    return index, documents


def search_vector_store(
    query: str,
    top_k: int = 6,
    candidate_k: int = 20,
) -> list[dict]:
    index, documents = load_vector_store()

    if index is None or not documents:
        return []

    query_embedding = np.asarray(
        embed_query(query),
        dtype="float32",
    )

    limit = min(candidate_k, len(documents))
    scores, indices = index.search(query_embedding, limit)

    results = []

    for score, index_position in zip(scores[0], indices[0]):
        if index_position < 0:
            continue

        document = dict(documents[index_position])
        document["score"] = round(float(score), 4)
        results.append(document)

    return results[:top_k]
