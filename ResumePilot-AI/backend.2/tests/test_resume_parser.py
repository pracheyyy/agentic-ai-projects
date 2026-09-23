from app.services.resume_parser import extract_resume


def test_txt_resume():

    content = b"""
    Prachi Patil

    Education
    B.Tech Information Technology

    Skills
    Python, Java, SQL, React

    Projects
    ResumePilot AI
    """

    text = extract_resume(
        "resume.txt",
        content
    )

    assert "Prachi Patil" in text

    assert "Python" in text

    assert "ResumePilot AI" in text