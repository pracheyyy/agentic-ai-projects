# ResumePilot AI Backend

FastAPI backend for ResumePilot AI.

## Features

- PDF/DOCX/TXT resume parsing
- JD requirement extraction
- Technical skill extraction
- Responsibility extraction
- Education and experience extraction
- Soft skill extraction
- Domain keyword extraction
- Requirement-level resume matching
- TF-IDF RAG evidence retrieval
- Explainable ATS readiness score
- Improvement recommendations

## Setup

From the `backend` folder:

```powershell
python -m pip install -r requirements.txt
```

## Run

```powershell
uvicorn app.main:app --reload
```

API docs:

http://127.0.0.1:8000/docs

## Test

```powershell
pytest
```

## Main endpoint

`POST /api/analyze`

Form fields:

- `resume`: PDF, DOCX, or TXT
- `job_description`: target job description
