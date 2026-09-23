from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.services.resume_parser import (
    extract_resume,
    parse_resume
)
from app.services.jd_parser import parse_job_description
from app.services.analysis_engine import analyze_requirements
from app.services.ats_scorer import calculate_ats_score
from app.services.improvement_engine import (
    generate_improvements,
    prioritize_recommendations
)


app = FastAPI(
    title="ResumePilot AI",
    description="AI-Powered Resume Optimization & Job Matching",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "ResumePilot AI API is running",
        "status": "success"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/api/resume/parse")
async def parse_resume_endpoint(
    resume: UploadFile = File(...)
):

    if not resume.filename:
        raise HTTPException(
            status_code=400,
            detail="Resume file is required."
        )

    content = await resume.read()

    try:
        text = extract_resume(
            resume.filename,
            content
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from resume."
        )

    return {
        "filename": resume.filename,
        "characters": len(text),
        "text": text
    }


@app.post("/api/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):

    if not resume.filename:
        raise HTTPException(
            status_code=400,
            detail="Resume file is required."
        )

    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job Description is required."
        )

    content = await resume.read()

    try:
        resume_data = parse_resume(
            resume.filename,
            content
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    try:
        jd_data = parse_job_description(
            job_description
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    analysis = analyze_requirements(
        resume_data,
        jd_data
    )

    ats_score = calculate_ats_score(
        resume_data,
        jd_data,
        analysis["matching"]
    )

    recommendations = generate_improvements(
        analysis
    )

    recommendations = prioritize_recommendations(
        recommendations
    )

    return {
        "resume": {
            "filename": resume_data["filename"],
            "skills": resume_data["skills"],
            "sections": resume_data["sections"]
        },

        "job_description": {
            "required_skills": jd_data["required_skills"],
            "soft_skills": jd_data["soft_skills"],
            "keywords": jd_data["keywords"],
            "experience_signals":
                jd_data["experience_signals"],
            "education_signals":
                jd_data["education_signals"],
            "experience_requirements":
                jd_data["experience_requirements"],
            "education_requirements":
                jd_data["education_requirements"],
            "sections":
                jd_data["sections"],
            "requirements":
                jd_data["requirements"]
        },

        "matching":
            analysis["matching"],

        "requirements":
            analysis["requirements"],

        "analysis_summary":
            analysis["summary"],

        "ats":
            ats_score,

        "recommendations":
            recommendations
    }
