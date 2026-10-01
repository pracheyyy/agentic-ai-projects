import html
import re


def normalize_article(article: dict) -> dict:
    clean = lambda value: re.sub(
        r"\s+",
        " ",
        html.unescape(value or "")
    ).strip()

    return {
        "id": article.get("id", ""),
        "title": clean(article.get("title")),
        "summary": clean(article.get("summary")),
        "url": article.get("url", "").strip(),
        "source": clean(article.get("source")),
        "published": article.get("published", ""),
        "scraped_at": article.get("scraped_at", ""),
        "type": article.get("type", "news"),
        "category": article.get("category", "Technology"),
    }
