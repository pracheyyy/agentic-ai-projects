from functools import lru_cache

from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embedding_model():
    return SentenceTransformer(MODEL_NAME)


def embed_documents(texts: list[str]):
    return get_embedding_model().encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=False,
    )


def embed_query(query: str):
    return get_embedding_model().encode(
        [query],
        normalize_embeddings=True,
        show_progress_bar=False,
    )
