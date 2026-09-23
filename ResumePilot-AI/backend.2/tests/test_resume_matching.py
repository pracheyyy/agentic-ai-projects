from app.services.resume_parser import parse_resume
from app.services.jd_parser import parse_job_description
from app.services.matching_engine import match_resume_to_jd


def test_resume_to_jd_matching():

    resume_content = b"""
    Prachi Patil

    Education
    B.Tech Information Technology

    Skills
    Python, Java, React, SQL, Git

    Experience
    Machine Learning Intern

    Projects
    ResumePilot AI
    """

    job_description = """
    We are looking for a Software Engineer.

    Requirements:
    Python
    React
    SQL
    Spring Boot
    Docker
    Git

    Bachelor's degree in Computer Science.
    """

    # Step 1: Parse resume
    resume_data = parse_resume(
        "resume.txt",
        resume_content
    )

    # Step 2: Parse JD
    jd_data = parse_job_description(
        job_description
    )

    # Step 3: Match
    result = match_resume_to_jd(
        resume_data,
        jd_data
    )

    # Exact matches
    assert "python" in result["matched"]
    assert "react" in result["matched"]
    assert "sql" in result["matched"]
    assert "git" in result["matched"]

    # Partial match
    assert "spring boot" in result["partial"]

    # Missing skill
    assert "docker" in result["missing"]

    # 4 exact + 0.5 partial out of 6
    assert result["match_percentage"] == 75.0