from app.services.matching_engine import (
    match_requirements,
    calculate_evidence_strength
)


def test_requirement_strong_match():

    resume_data = {
        "raw_text": """
        Developed REST APIs using FastAPI and Python.
        Built backend services with MongoDB.
        """
    }

    jd_data = {
        "requirements": [
            {
                "text": "Developed REST APIs using FastAPI",
                "category": "responsibility",
                "importance": "high"
            }
        ]
    }

    result = match_requirements(
        resume_data,
        jd_data
    )

    assert result["matched_count"] == 1
    assert result["missing_count"] == 0


def test_requirement_missing():

    resume_data = {
        "raw_text": """
        Developed web applications using
        JavaScript and React.
        """
    }

    jd_data = {
        "requirements": [
            {
                "text": "Experience with Kubernetes",
                "category": "technical_skill",
                "importance": "high"
            }
        ]
    }

    result = match_requirements(
        resume_data,
        jd_data
    )

    assert result["missing_count"] == 1
    assert result["matched_count"] == 0