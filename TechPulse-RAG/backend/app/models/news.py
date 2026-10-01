from pydantic import BaseModel, HttpUrl


class NewsArticle(BaseModel):
    id: str
    title: str
    summary: str
    url: HttpUrl
    source: str
    published: str
    scraped_at: str
    type: str = "news"
