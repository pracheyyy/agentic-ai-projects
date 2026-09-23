from app.services.jd_parser import parse_job_description


def test_parse_job_description():

    jd = """
    Software Engineer Intern

    Responsibilities:
    - Develop REST APIs using FastAPI
    - Build backend services using Python
    - Work with MongoDB databases
    - Debug and test software applications

    Requirements:
    - Strong knowledge of Python and SQL
    - Experience with Git and GitHub
    - Good problem solving and communication skills

    Qualifications:
    - Bachelor's degree in Computer Science or Information Technology

    Preferred Qualifications:
    - Experience with Docker
    """

    result = parse_job_description(jd)

    assert "python" in result["required_skills"]
    assert "fastapi" in result["required_skills"]
    assert "mongodb" in result["required_skills"]

    assert "problem solving" in result["soft_skills"]
    assert "communication" in result["soft_skills"]

    assert len(result["requirements"]) > 0

    categories = {
        item["category"]
        for item in result["requirements"]
    }

    assert "technical_skill" in categories
    assert "responsibility" in categories
    assert "education" in categories