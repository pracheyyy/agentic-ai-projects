from app.services.rag_retriever import (
    retrieve_evidence,
    retrieve_requirement_evidence,
    classify_evidence
)


def test_retrieve_evidence():

    resume = """
    Prachi Patil

    Developed REST APIs using FastAPI and Python.
    Built backend services with MongoDB.

    Worked with Git and GitHub.
    """

    result = retrieve_evidence(
        resume_text=resume,
        query="REST APIs FastAPI",
        top_k=2
    )

    assert isinstance(result, list)
    assert len(result) > 0
    assert "text" in result[0]
    assert "score" in result[0]


def test_requirement_evidence():

    resume = """
    Prachi Patil

    Developed REST APIs using FastAPI and Python.
    Built backend services with MongoDB.
    """

    result = retrieve_requirement_evidence(
        resume_text=resume,
        requirement="REST APIs using FastAPI",
        top_k=2
    )

    assert "requirement" in result
    assert "relevance" in result
    assert "evidence" in result
    assert len(result["evidence"]) > 0


def test_missing_evidence():

    result = classify_evidence([])

    assert result == "missing"
