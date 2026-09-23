from app.services.improvement_engine import (
    generate_improvements,
    prioritize_recommendations
)


def test_generate_improvements():

    analysis_result = {
        "requirements": [
            {
                "requirement": "FastAPI",
                "category": "technical_skill",
                "importance": "high",
                "status": "missing",
                "evidence_strength": 0,
                "evidence": []
            },
            {
                "requirement": "Develop REST APIs",
                "category": "responsibility",
                "importance": "high",
                "status": "partial",
                "evidence_strength": 2,
                "evidence": [
                    {
                        "text": "Built backend APIs",
                        "score": 0.42
                    }
                ]
            },
            {
                "requirement": "Python",
                "category": "technical_skill",
                "importance": "high",
                "status": "matched",
                "evidence_strength": 3,
                "evidence": [
                    {
                        "text": "Developed applications using Python",
                        "score": 0.88
                    }
                ]
            }
        ]
    }

    recommendations = generate_improvements(
        analysis_result
    )

    assert len(recommendations) == 3
    assert recommendations[0]["category"] == "technical_skill"
    assert recommendations[0]["priority"] == "high"
    assert "FastAPI" in recommendations[0]["recommendation"]


def test_prioritize_recommendations():

    recommendations = [
        {
            "requirement": "Python",
            "priority": "low",
            "importance": "high"
        },
        {
            "requirement": "FastAPI",
            "priority": "high",
            "importance": "high"
        },
        {
            "requirement": "Git",
            "priority": "medium",
            "importance": "medium"
        }
    ]

    result = prioritize_recommendations(
        recommendations
    )

    assert result[0]["requirement"] == "FastAPI"
