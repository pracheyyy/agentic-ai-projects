import hashlib
import html
import re
from datetime import datetime, timezone

import feedparser

RSS_FEEDS = {
    "TechCrunch": "https://techcrunch.com/feed/",
    "Ars Technica": "https://feeds.arstechnica.com/arstechnica/index",
}


def clean_html(text: str) -> str:
    text = html.unescape(text or "")
    text = re.sub(r"<script.*?>.*?</script>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<style.*?>.*?</style>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def parse_entry(entry, source: str) -> dict:
    url = entry.get("link", "").strip()
    title = clean_html(entry.get("title", ""))
    summary = clean_html(entry.get("summary", "") or entry.get("description", ""))

    return {
        "id": hashlib.sha256((url or title).encode("utf-8")).hexdigest()[:16],
        "title": title,
        "summary": summary,
        "url": url,
        "source": source,
        "published": entry.get("published", "") or entry.get("updated", ""),
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "type": "news",
    }


def scrape_feed(source: str, url: str, limit: int) -> list[dict]:
    feed = feedparser.parse(url)

    if getattr(feed, "bozo", False) and not feed.entries:
        raise RuntimeError(f"Could not read RSS feed: {source}")

    articles = []
    for entry in feed.entries[:limit]:
        article = parse_entry(entry, source)
        if article["title"] and article["url"]:
            articles.append(article)

    return articles


def scrape_all_feeds(limit_per_feed: int = 30) -> list[dict]:
    articles = []

    for source, url in RSS_FEEDS.items():
        try:
            articles.extend(scrape_feed(source, url, limit_per_feed))
        except Exception as exc:
            print(f"[RSS ERROR] {source}: {exc}")

    unique = {article["url"]: article for article in articles}
    return list(unique.values())
