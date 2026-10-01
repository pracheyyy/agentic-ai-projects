import json
from pathlib import Path

from app.scraper.cleaner import normalize_article
from app.scraper.rss_scraper import scrape_all_feeds

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_FILE = BASE_DIR / "data" / "raw" / "news.json"


def save_articles(articles: list[dict]) -> None:
    RAW_FILE.parent.mkdir(parents=True, exist_ok=True)
    RAW_FILE.write_text(
        json.dumps(articles, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_articles() -> list[dict]:
    if not RAW_FILE.exists():
        return []

    try:
        return json.loads(RAW_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []


def refresh_news(limit: int = 30) -> dict:
    articles = [
        normalize_article(article)
        for article in scrape_all_feeds(limit)
    ]

    save_articles(articles)

    return {
        "message": "News ingestion completed",
        "count": len(articles),
        "articles": articles,
    }


def get_latest_news(limit: int = 20) -> list[dict]:
    articles = load_articles()

    if not articles:
        articles = refresh_news(limit)["articles"]

    return articles[:limit]
