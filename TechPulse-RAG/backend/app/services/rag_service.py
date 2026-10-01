import os

from app.services.knowledge_service import load_knowledge_documents
from app.services.llm_service import generate_answer
from app.services.news_service import load_articles, refresh_news
from app.services.vector_store import build_vector_store, search_vector_store


# Cosine similarity because embeddings are normalized and FAISS uses inner product.
# This threshold prevents unrelated documents from being presented as answers.
MIN_SIMILARITY = float(os.getenv("MIN_SIMILARITY", "0.38"))


def build_index() -> dict:
    news = load_articles()

    if not news:
        news = refresh_news(30)["articles"]

    knowledge = load_knowledge_documents()

    documents = knowledge + news

    if not documents:
        raise ValueError("No TechPulse knowledge or news documents are available.")

    return build_vector_store(documents)


def retrieve(question: str, top_k: int = 6) -> list[dict]:
    results = search_vector_store(
        question,
        top_k=top_k,
        candidate_k=max(20, top_k * 3),
    )

    # If there is no index, build it once and try again.
    if not results:
        build_index()
        results = search_vector_store(
            question,
            top_k=top_k,
            candidate_k=max(20, top_k * 3),
        )

    # Remove weak semantic matches.
    relevant = [
        result
        for result in results
        if float(result.get("score", 0)) >= MIN_SIMILARITY
    ]

    return relevant


def ask_question(question: str, top_k: int = 6) -> dict:
    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty.")

    sources = retrieve(question, top_k)

    if not sources:
        return {
            "question": question,
            "answer": (
                "I don't have enough information in my TechPulse knowledge "
                "base to answer that reliably."
            ),
            "sources": [],
            "source_count": 0,
            "generation": "insufficient-context",
        }

    answer = generate_answer(question, sources)

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "source_count": len(sources),
        "generation": (
            os.getenv("LLM_MODEL", "openai/gpt-oss-20b:fastest")
            if os.getenv("HF_TOKEN")
            else "retrieval-fallback"
        ),
    }
