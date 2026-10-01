from fastapi import APIRouter, HTTPException
from app.services.news_service import get_latest_news, refresh_news

router = APIRouter(prefix="/news", tags=["News"])


@router.get("/")
def get_news(limit: int = 20):
    if not 1 <= limit <= 100:
        raise HTTPException(400, "limit must be between 1 and 100")
    return {"count": len(get_latest_news(limit)), "articles": get_latest_news(limit)}


@router.post("/scrape")
def scrape_news(limit: int = 30):
    if not 1 <= limit <= 100:
        raise HTTPException(400, "limit must be between 1 and 100")
    return refresh_news(limit)
