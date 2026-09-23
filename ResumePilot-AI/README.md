# 🚀 ResumePilot AI

### AI-Powered Resume Optimization & Job Matching System

ResumePilot AI is an intelligent resume analysis platform that evaluates a candidate's resume against a target Job Description (JD).

Instead of relying only on simple keyword matching, ResumePilot breaks a Job Description into individual requirements, maps those requirements against the resume, retrieves relevant resume evidence using RAG, calculates a transparent ATS-style readiness score, and generates actionable improvement recommendations.

> **Goal:** Help candidates understand how well their resume matches a specific job and exactly what can be improved — without encouraging fabricated skills or experience.

---

## ✨ Features

### 📄 Resume Parsing

Supports:

- PDF
- DOCX
- TXT

The resume parser extracts:

- Raw resume text
- Technical skills
- Education
- Experience
- Projects
- Certifications
- Achievements
- Resume sections

### 🧠 Job Description Intelligence

ResumePilot analyzes the complete Job Description instead of checking only technical skills.

It extracts:

- Technical skills
- Responsibilities
- Qualifications
- Experience requirements
- Education requirements
- Soft skills
- Domain keywords
- Important JD requirements

Each requirement is represented independently.

Example:

```json
{
  "text": "Develop REST APIs using FastAPI",
  "category": "responsibility",
  "importance": "high"
}
```

### 🎯 Requirement-Level Matching

Every extracted JD requirement is compared against the resume.

Current matching states:

```text
Matched
Partial
Weak
Missing
```

Evidence strength:

```text
3 → Strong
2 → Moderate
1 → Weak
0 → Missing
```

### 🔎 RAG-Based Evidence Retrieval

ResumePilot currently uses a lightweight TF-IDF retrieval pipeline to find relevant evidence from the resume for each JD requirement.

```text
Resume
   ↓
Text Chunking
   ↓
TF-IDF Vectorization
   ↓
Cosine Similarity
   ↓
Relevant Resume Evidence
```

### 📊 Transparent ATS-Style Scoring

Current ResumePilot scoring model:

| Category | Weight |
|---|---:|
| Technical Skills | 30% |
| Responsibilities | 25% |
| Experience | 15% |
| Education | 10% |
| Domain Keywords | 10% |
| Soft Skills | 5% |
| Resume Structure | 5% |
| **Total** | **100%** |

> These weights are ResumePilot's own scoring model and are not intended to represent the exact scoring algorithm used by every commercial ATS.

### 💡 Resume Improvement Recommendations

Recommendations are based on:

- Requirement
- Category
- Importance
- Match status
- Retrieved evidence

The system avoids recommending fabricated skills or experience.

### 🎯 Recommendation Prioritization

Recommendations are categorized as:

- High
- Medium
- Low

---

# 🏗️ System Architecture

```text
                         ResumePilot AI
                              │
              ┌───────────────┴───────────────┐
              │                               │
           Resume                      Job Description
              │                               │
              ▼                               ▼
       Resume Parser                     JD Parser
              │                               │
              ▼                               ▼
        Resume Data                 Requirement Extraction
                                              │
                         ┌────────────────────┼───────────────────┐
                         │                    │                   │
                      Skills          Responsibilities      Qualifications
                         │                    │                   │
                         └────────────────────┼───────────────────┘
                                              │
                                              ▼
                                      Matching Engine
                                              │
                                              ▼
                                      Requirement Status
                                              │
                                              ▼
                                      RAG Evidence Retrieval
                                              │
                                              ▼
                                       Resume Evidence
                                              │
                                              ▼
                                         ATS Scoring
                                              │
                                              ▼
                                    Improvement Engine
                                              │
                                              ▼
                                         Results
```

---

# 🛠️ Tech Stack

### Backend

- Python
- FastAPI
- Uvicorn
- PyMuPDF
- python-docx
- scikit-learn
- pytest

### Resume Processing

- PyMuPDF
- python-docx
- Custom text normalization
- Rule-based section detection

### Matching

- Requirement-level matching
- Skill normalization
- Related skill mapping
- Evidence strength calculation

### RAG

Current implementation:

- TF-IDF
- Cosine Similarity
- Resume chunk retrieval

### Frontend

- HTML5
- CSS3
- JavaScript
- Session Storage
- REST API integration

---

# 📁 Project Structure

```text
ResumePilot-AI/
│
├── frontend/
│   ├── index.html
│   ├── pages/
│   │   ├── analyze.html
│   │   ├── analysis.html
│   │   └── results.html
│   ├── css/
│   │   ├── style.css
│   │   ├── analyze.css
│   │   ├── analysis.css
│   │   └── results.css
│   ├── js/
│   │   ├── main.js
│   │   ├── analyze.js
│   │   ├── analysis.js
│   │   └── results.js
│   └── assets/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── resume_parser.py
│   │       ├── jd_parser.py
│   │       ├── matching_engine.py
│   │       ├── rag_retriever.py
│   │       ├── analysis_engine.py
│   │       ├── ats_scorer.py
│   │       └── improvement_engine.py
│   ├── tests/
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── .gitignore
│   └── README.md
│
└── README.md
```

---

# 🔄 Application Workflow

```text
1. Upload Resume
        ↓
2. Paste Job Description
        ↓
3. Resume Parsing
        ↓
4. JD Intelligence
        ↓
5. Requirement Extraction
        ↓
6. Requirement Matching
        ↓
7. RAG Evidence Retrieval
        ↓
8. ATS-Style Scoring
        ↓
9. Improvement Generation
        ↓
10. Results Dashboard
```

---

# 🔌 API

## Health Check

```http
GET /
```

## Health

```http
GET /health
```

## Resume Parsing

```http
POST /api/resume/parse
```

Form field:

```text
resume
```

Supported formats:

```text
PDF
DOCX
TXT
```

## Resume + JD Analysis

```http
POST /api/analyze
```

Form fields:

```text
resume
job_description
```

The endpoint returns:

```text
Resume Data
+
JD Data
+
Requirements
+
Matching Results
+
RAG Evidence
+
ATS Score
+
Recommendations
```

---

# 🚀 Local Setup

## 1. Clone the Repository

```bash
git clone https://github.com/pracheyyy/agentic-ai-projects.git
cd agentic-ai-projects/ResumePilot-AI
```

## 2. Create Virtual Environment

Navigate to the backend:

```bash
cd backend
```

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🌐 Run Frontend

Open the frontend using a local development server such as VS Code Live Server.

Open:

```text
frontend/index.html
```

Application flow:

```text
Home
 ↓
Analyze
 ↓
Upload Resume
 ↓
Paste Job Description
 ↓
Analyze
 ↓
Results
```

---

# 🧪 Testing

From the backend directory:

```bash
pytest
```

Tests cover:

- Resume parsing
- JD parsing
- Requirement extraction
- Matching
- RAG retrieval
- Analysis
- ATS scoring
- Improvement generation

---

# 🧩 Current RAG Architecture

The current RAG implementation is intentionally lightweight.

```text
Resume Text
     ↓
Line-based Chunking
     ↓
TF-IDF Vectorization
     ↓
Query Vector
     ↓
Cosine Similarity
     ↓
Top-K Evidence
```

Example:

```text
JD Requirement
      ↓
"Develop REST APIs using FastAPI"
      ↓
Retriever
      ↓
Resume Chunks
      ↓
Similarity Scores
      ↓
Top Relevant Evidence
```

---

# 🔮 Roadmap

## Phase 1 — Core ATS Engine ✅

- [x] Resume parsing
- [x] PDF/DOCX/TXT support
- [x] JD parsing
- [x] Requirement extraction
- [x] Skill matching
- [x] Requirement-level matching
- [x] ATS-style scoring
- [x] Resume structure analysis
- [x] Improvement recommendations
- [x] Frontend/backend integration
- [x] Automated tests

## Phase 2 — Evidence-Based RAG 🚧

- [x] Resume chunking
- [x] TF-IDF retrieval
- [x] Cosine similarity
- [x] Requirement-level evidence retrieval
- [ ] Evidence-driven final matching status
- [ ] Better semantic matching
- [ ] Improved evidence scoring
- [ ] Requirement importance-aware scoring

## Phase 3 — Semantic RAG 🔮

Planned:

```text
Resume
 ↓
Semantic Chunking
 ↓
Embeddings
 ↓
Vector Database
 ↓
Semantic Retrieval
 ↓
Reranking
 ↓
Evidence
```

Planned technologies:

- Sentence Transformers
- Qdrant
- BM25
- Hybrid Retrieval
- Reranking

## Phase 4 — LLM Reasoning 🔮

Planned:

- LLM-based requirement analysis
- Grounded explanations
- Evidence-aware reasoning
- Resume bullet analysis
- Context-aware recommendations
- Structured LLM outputs

The LLM should reason over retrieved resume evidence rather than inventing information.

## Phase 5 — Resume Optimization 🔮

Planned:

```text
Current Resume
      ↓
JD Analysis
      ↓
Missing / Weak Requirements
      ↓
Improvement Suggestions
      ↓
Resume Optimization
      ↓
Projected ResumePilot Score
```

Potential features:

- Resume bullet improvement
- Keyword placement suggestions
- Section optimization
- Job-specific resume versions
- Before/after comparison
- Score projection

> Projected scores will represent ResumePilot's internal model and should not be interpreted as a guaranteed score from an external ATS.

## Phase 6 — Resume Version Management 🔮

Planned:

- Save multiple resumes
- Save multiple job descriptions
- Resume versions
- Analysis history
- Resume ↔ JD history
- Compare resume versions
- Track score changes

## Phase 7 — Production Deployment 🔮

Planned:

- Docker
- PostgreSQL
- Authentication
- Cloud deployment
- API security
- Rate limiting
- Production logging
- Monitoring

---

# 🔐 Design Principles

### Evidence First

Recommendations should be grounded in information actually present in the resume.

### No Fabrication

The system should never encourage candidates to claim:

- Skills they do not have
- Experience they did not obtain
- Projects they did not build
- Qualifications they do not possess

### Explainable Scoring

The final score should be decomposable into understandable categories.

```text
ATS Score
   ↓
Technical Skills
Responsibilities
Experience
Education
Domain Keywords
Soft Skills
Structure
```

### Requirement-Level Analysis

Instead of treating a JD as a single document:

```text
JD
 ↓
Individual Requirements
 ↓
Evidence
 ↓
Match Status
```

---

# 🧠 Why RAG?

Traditional keyword matching can tell us:

```text
"FastAPI" exists in resume
```

RAG allows ResumePilot to retrieve supporting context:

```text
Where is FastAPI mentioned?

What project or experience contains it?

What evidence supports the requirement?

How relevant is that evidence?
```

This moves the system from:

```text
Keyword Matching
```

toward:

```text
Evidence-Based Resume Evaluation
```

---

# 📌 Example

Suppose the JD contains:

```text
Develop REST APIs using FastAPI.

Work with MongoDB.

Collaborate with cross-functional teams.
```

ResumePilot converts these into requirements:

```text
1. Develop REST APIs using FastAPI
2. MongoDB
3. Cross-functional collaboration
```

Then:

```text
Requirement
      ↓
Resume Search
      ↓
Evidence
      ↓
Match Status
      ↓
ATS Contribution
      ↓
Recommendation
```

Example:

```text
FastAPI
→ Matched
→ Strong evidence

MongoDB
→ Matched
→ Strong evidence

Cross-functional collaboration
→ Partial
→ Limited evidence
```

---

# 📊 Project Status

### Current Version: `v1.0 — Core ATS + RAG Foundation`

```text
Resume Parsing              ✅
JD Intelligence             ✅
Requirement Extraction      ✅
Requirement Matching        ✅
TF-IDF RAG                  ✅
Evidence Retrieval          ✅
ATS-Style Scoring           ✅
Recommendations             ✅
Frontend Integration        ✅
Backend API                 ✅
Automated Testing           ✅

Semantic Embeddings         🚧
Qdrant                      🔮
Hybrid Retrieval            🔮
Reranking                   🔮
LLM Reasoning               🔮
Resume Optimization         🔮
Version Management          🔮
Production Deployment       🔮
```

---

# 🎯 Vision

ResumePilot AI aims to evolve from a basic ATS checker into an **evidence-grounded resume intelligence platform**.

Long-term architecture:

```text
                   ResumePilot AI
                         │
             ┌───────────┴───────────┐
             │                       │
          Resume                  Job Description
             │                       │
             ▼                       ▼
       Resume Parser            JD Intelligence
             │                       │
             └───────────┬───────────┘
                         ▼
                Requirement Engine
                         │
                         ▼
                  Semantic RAG
                         │
                         ▼
                  Resume Evidence
                         │
                         ▼
                 Evidence Evaluator
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
        ATS Scoring           Improvement Engine
             │                       │
             └───────────┬───────────┘
                         ▼
                  Resume Insights
```

---

## 👨‍💻 Author

**Prachi Patil**

B.Tech Information Technology  
JSPM Rajarshri Shahu College of Engineering, Pune

---

## ⭐ Project

If you find this project useful, consider giving the repository a ⭐.

Built as an ongoing AI/ML engineering project focused on:

**RAG • NLP • Resume Intelligence • ATS Analysis • FastAPI • AI Systems**
