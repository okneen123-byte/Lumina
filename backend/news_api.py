# backend/news_api.py
import requests
from config import NEWS_API_KEY
import logging

logger = logging.getLogger("news_api")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)


def fetch_news_from_api(category="general", language="en", page_size=40):
    """Holt aktuelle News von der NewsAPI."""
    url = (
        f"https://newsapi.org/v2/top-headlines?"
        f"category={category}&language={language}&pageSize={page_size}&apiKey={NEWS_API_KEY}"
    )

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])

        results = []
        for a in articles:
            results.append({
                "title": a.get("title", ""),
                "description": a.get("description", ""),
                "url": a.get("url", ""),
                "source": a.get("source", {}).get("name", ""),
                "published_at": a.get("publishedAt", "")
            })

        logger.info(f"{len(results)} Artikel von API geladen ({category}, {language})")
        return results

    except Exception as e:
        logger.exception("Fehler beim Abrufen der News: %s", e)
        return []


def compute_importance(article):
    """Berechnet einen einfachen Wichtigkeitswert für Artikel."""
    score = 0.0
    if article.get("description"):
        score += len(article["description"]) / 100
    if article.get("title"):
        score += len(article["title"]) / 50
    return round(min(score, 10.0), 2)
