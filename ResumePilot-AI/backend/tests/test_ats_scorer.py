from app.services.ats_scorer import calculate_ats_score


def test_calculate_ats_score():

    resume_data = {
        "skills": [
            "python",
            "fastapi",
            "mongodb"
        ],
        "sections": {
            "education": [
                "B.Tech Information Technology"
            ],
            "skills": [
                "Python, FastAPI, MongoDB"
            ],
            "experience": [
                "Software Developer Intern"
            ],
            "projects": [
                "ResumePilot AI"
            ]
        }
    }

    jd_data = {}

    matching_result = {
        "requirements": [
            {
                "requirement": "Python",
                "category": "technical_skill",
                "importance": "high",
                "status": "matched"
            },
            {
                "requirement": "FastAPI",
                "category": "technical_skill",
                "importance": "high",
                "status": "matched"
            },
            {
                "requirement": "Develop REST APIs",
                "category": "responsibility",
                "importance": "high",
                "status": "partial"
            },
            {
                "requirement": "Communication",
                "category": "soft_skill",
                "importance": "medium",
                "status": "missing"
            },
            {
                "requirement": "B.Tech",
                "category": "education",
                "importance": "high",
                "status": "matched"
            }
        ]
    }

    result = calculate_ats_score(
        resume_data,
        jd_data,
        matching_result
    )

    assert "ats_score" in result
    assert 0 <= result["ats_score"] <= 100
    assert "technical_skills" in result["components"]
    assert "responsibilities" in result["components"]
    assert "education" in result["components"]
    assert "soft_skills" in result["components"]
    assert result["summary"]["total_requirements"] == 5
