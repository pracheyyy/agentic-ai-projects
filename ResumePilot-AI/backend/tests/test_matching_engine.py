from app.services.matching_engine import (
    match_resume_to_jd,
    match_requirements
)


def test_skill_matching():

    resume_data = {
        "skills": [
            "python",
            "javascript",
            "java"
        ]
    }

    jd_data = {
        "required_skills": [
            "python",
            "javascript",
            "fastapi"
        ]
    }

    result = match_resume_to_jd(
        resume_data,
        jd_data
    )

    assert "python" in result["matched"]
    assert "javascript" in result["matched"]
    assert "fastapi" in result["missing"]


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
