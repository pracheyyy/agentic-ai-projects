# TechPulse RAG — Complete IT Knowledge + Tech News

The UI is unchanged. The frontend talks to the FastAPI backend.

The final answer generation now uses an **open-weight LLM through Hugging Face Inference Providers** instead of Gemini.

## Architecture

```text
                         TECHPULSE KNOWLEDGE
                                  |
                    +-------------+-------------+
                    |                           |
                    v                           v
             TECH KNOWLEDGE                 TECH NEWS
             Documentation                 RSS Feeds
             Tutorials                     Articles
             Concepts                      Updates
                    |                           |
                    +-------------+-------------+
                                  |
                               Chunking
                                  |
                              Embeddings
                                  |
                                FAISS
                                  |
                              Retrieval
                                  |
                         Similarity Threshold
                                  |
                         Relevant context only
                                  |
                         Hugging Face Router
                                  |
                        openai/gpt-oss-20b
                                  |
                          Answer + Sources
```

## LLM used

TechPulse uses **`openai/gpt-oss-20b`**, an open-weight model, through Hugging Face Inference Providers. Hugging Face provides an OpenAI-compatible chat-completions endpoint, so the existing FastAPI RAG flow only needs a small LLM-service change.

The project does **not** use the Gemini API anymore.

Hugging Face supports provider selection policies such as `:fastest`, `:cheapest`, and `:preferred`. This project defaults to `:fastest` through:

```text
LLM_MODEL=openai/gpt-oss-20b:fastest
```

Inference Providers still have usage limits/credits and are not an unlimited free API. A Hugging Face token is required for generated answers. Without one, TechPulse automatically falls back to retrieval-only responses.

## What the chatbot can cover

The starter knowledge base covers IT topics such as:

- Programming
- Data structures and algorithms
- AI/ML
- RAG
- Web development
- Backend development
- Databases and SQL
- Cloud and DevOps
- Cybersecurity
- Operating systems
- Computer networks

Technology news is added from permitted RSS feeds.

The knowledge corpus is local Markdown content. Add more Markdown files under `backend/data/knowledge/` to expand the assistant.

## Relevance protection

FAISS returns similarity scores. TechPulse applies `MIN_SIMILARITY` before passing results to the answer generator.

If nothing passes the threshold:

```text
I don't have enough information in my TechPulse knowledge base to answer that reliably.
```

This prevents unrelated news from being presented as an answer.

## Sources

Current news ingestion uses:

- TechCrunch RSS
- Ars Technica RSS

The app does not bypass robots.txt, CAPTCHAs, paywalls, login walls or other access controls.

## Windows setup

Open PowerShell in:

```text
TechPulse-RAG\backend
```

Create the virtual environment using your existing Anaconda Python:

```powershell
C:\Users\praci\anaconda3\python.exe -m venv venv
```

Activate it:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run the backend:

```powershell
python -m uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Configure Hugging Face

Open:

```text
backend/.env
```

Add your Hugging Face token:

```text
HF_TOKEN=hf_your_token_here
```

Keep:

```text
LLM_MODEL=openai/gpt-oss-20b:fastest
HF_BASE_URL=https://router.huggingface.co/v1
```

The token should have permission to make calls to Hugging Face Inference Providers.

## First-time RAG setup

In Swagger, run:

```text
1. GET  /health
2. POST /api/news/scrape
3. POST /api/rag/index
4. POST /api/rag/ask
```

The first indexing run downloads:

```text
sentence-transformers/all-MiniLM-L6-v2
```

and creates:

```text
backend/data/vectorstore/techpulse.index
backend/data/vectorstore/documents.json
```

## Run the frontend

Keep the backend terminal running.

Open the project root in VS Code and use Live Server on:

```text
index.html
```

The frontend will normally run at:

```text
http://127.0.0.1:5500
```

The frontend calls:

```text
POST http://127.0.0.1:8000/api/rag/ask
```

and:

```text
GET http://127.0.0.1:8000/api/news/
```

## Test questions

### Technical knowledge

```text
What is a linked list?
Explain binary search.
What is RAG?
How do embeddings work?
What is the difference between TCP and UDP?
What is normalization in DBMS?
What is dependency injection?
What is REST API?
What is Docker?
Explain supervised learning.
```

### Technology news

```text
What are the latest AI developments?
What are the latest cybersecurity trends?
What recent technology news is related to AI agents?
```

### Relevance test

Ask something outside the indexed knowledge:

```text
Which are the top 10 MNCs in the world?
```

If the retrieved context is below the configured threshold, TechPulse should refuse to invent an answer.

## Expand the knowledge base

Add Markdown files:

```text
backend/data/knowledge/
├── programming/
├── ai_ml/
├── rag/
├── web_development/
├── backend/
├── databases/
├── cloud_devops/
├── cybersecurity/
└── cs_fundamentals/
```

After adding or editing knowledge, run:

```text
POST /api/rag/index
```

to rebuild the unified FAISS index.

## Important

The current system is an IT-focused RAG assistant, not a general-purpose chatbot. It answers from the knowledge and news documents indexed by TechPulse.
