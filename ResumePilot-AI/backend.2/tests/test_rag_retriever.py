from app.services.rag_retriever import retrieve_evidence


def test_rag_retrieval():

    resume_text = """
    Prachi Patil

    Skills
    Python, Java, React

    Experience
    Developed REST APIs using FastAPI and Python.

    Projects
    ResumePilot AI
    Built a RAG-based application using Python.
    """

    results = retrieve_evidence(
        resume_text,
        "Python REST API",
        top_k=2
    )

    assert len(results) == 2

    assert any(
        "REST APIs" in result["text"]
        for result in results
    )

    assert all(
        "score" in result
        for result in results
    )