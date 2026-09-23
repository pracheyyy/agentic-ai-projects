from app.services.analysis_engine import analyze_requirements


def test_analyze_requirements():

    resume_data = {
        "raw_text": """
        Prachi Patil

        Developed REST APIs using FastAPI and Python.
        Built backend services using MongoDB.

        Skills:
        Python
        FastAPI
        MongoDB
        Git
        """
    }

    jd_data = {
        "requirements": [
            {
                "text": "Develop REST APIs using FastAPI",
                "category": "responsibility",
                "importance": "high"
            },
            {
                "text": "Experience with Kubernetes",
                "category": "technical_skill",
                "importance": "high"
            }
        ]
    }

    result = analyze_requirements(
        resume_data,
        jd_data
    )

    assert "requirements" in result

    assert len(
        result["requirements"]
    ) == 2

    first = result["requirements"][0]

    assert first["requirement"] == (
        "Develop REST APIs using FastAPI"
    )

    assert first["status"] == "matched"

    assert first["evidence_strength"] == 3

    assert len(
        first["evidence"]
    ) > 0

    second = result["requirements"][1]

    assert second["status"] == "missing"