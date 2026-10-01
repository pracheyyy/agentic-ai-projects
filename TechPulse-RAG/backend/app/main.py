from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.news import router as news_router
from app.routes.rag import router as rag_router

app = FastAPI(
    title="TechPulse RAG API",
    description="IT knowledge + technology news RAG assistant.",
    version="4.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(news_router, prefix="/api")
app.include_router(rag_router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "TechPulse RAG API is running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
