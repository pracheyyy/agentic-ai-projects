import re
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
KNOWLEDGE_DIR = BASE_DIR / "data" / "knowledge"


def clean_text(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"#{1,6}\s*", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def chunk_text(text: str, chunk_size: int = 900, overlap: int = 120) -> list[str]:
    words = clean_text(text).split()

    if not words:
        return []

    chunks = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))

        if end == len(words):
            break

        start = max(end - overlap, start + 1)

    return chunks


def load_knowledge_documents() -> list[dict]:
    documents = []

    if not KNOWLEDGE_DIR.exists():
        return documents

    for path in sorted(KNOWLEDGE_DIR.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        category = path.parent.name

        for index, chunk in enumerate(chunk_text(text)):
            documents.append({
                "id": f"{path.stem}-{index}",
                "title": path.stem.replace("_", " ").title(),
                "summary": chunk,
                "url": "",
                "source": f"TechPulse Knowledge · {category}",
                "published": "",
                "scraped_at": "",
                "type": "knowledge",
                "category": category,
            })

    return documents
