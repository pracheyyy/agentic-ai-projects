from typing import List, Dict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


DEFAULT_THRESHOLD = 0.10


# =========================================================
# Text chunking
# =========================================================

def split_into_chunks(
    text: str,
    chunk_size: int = 4
) -> List[str]:

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    chunks = []

    for i in range(
        0,
        len(lines),
        chunk_size
    ):

        chunk = "\n".join(
            lines[i:i + chunk_size]
        )

        if chunk.strip():
            chunks.append(chunk)

    return chunks


# =========================================================
# Normalize query
# =========================================================

def normalize_query(query: str) -> str:

    return " ".join(
        query.lower()
        .strip()
        .split()
    )


# =========================================================
# Retrieve evidence
# =========================================================

def retrieve_evidence(
    resume_text: str,
    query: str,
    top_k: int = 3,
    threshold: float = DEFAULT_THRESHOLD
) -> List[Dict]:

    if not resume_text.strip():
        return []

    if not query.strip():
        return []

    chunks = split_into_chunks(
        resume_text
    )

    if not chunks:
        return []

    query = normalize_query(
        query
    )

    # -----------------------------------------------------
    # Create documents
    # -----------------------------------------------------

    documents = chunks + [query]

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2)
    )

    matrix = vectorizer.fit_transform(
        documents
    )

    chunk_vectors = matrix[:-1]

    query_vector = matrix[-1]

    # -----------------------------------------------------
    # Similarity
    # -----------------------------------------------------

    similarities = cosine_similarity(
        query_vector,
        chunk_vectors
    ).flatten()

    ranked_indexes = (
        similarities
        .argsort()[::-1]
    )

    results = []

    # -----------------------------------------------------
    # Return top evidence
    # -----------------------------------------------------

    for index in ranked_indexes:

        score = float(
            similarities[index]
        )

        if score < threshold:
            continue

        results.append({
            "text": chunks[index],
            "score": round(
                score,
                4
            )
        })

        if len(results) >= top_k:
            break

    return results