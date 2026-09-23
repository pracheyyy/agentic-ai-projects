from app.services.matching_engine import match_resume_to_jd


def test_resume_matching():

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
            "fastapi",
            "java"
        ]
    }

    result = match_resume_to_jd(
        resume_data,
        jd_data
    )

    assert "python" in result["matched"]
    assert "java" in result["matched"]
    assert "fastapi" in result["missing"]
