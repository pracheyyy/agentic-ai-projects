from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.rag_service import build_index, ask_question

router = APIRouter(prefix="/rag", tags=["RAG"])


class AskRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=1500)
    top_k: int = Field(default=6, ge=1, le=10)


@router.post("/index")
def create_index():
    try:
        return build_index()
    except Exception as exc:
        raise HTTPException(500, f"Indexing failed: {exc}")


@router.post("/ask")
def ask(request: AskRequest):
    try:
        return ask_question(request.question, request.top_k)
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    except Exception as exc:
        raise HTTPException(500, f"RAG error: {exc}")
