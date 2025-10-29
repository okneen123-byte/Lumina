# backend/news_api.py
import requests
from config import NEWS_API_KEY
import logging

logger = logging.getLogger("news_api")

BASE_URL = "https://newsdata.io/api/1/news"

def fetch_news_from_api(category="general", language="en", page_size=40):
    """Holt News von NewsData.io."""
    params = {
        "apikey": NEWS_API_KEY,
        "language": language,
        "category": category,
        "country": "us" if language == "en" else "de",
        "page": 1  # NewsData erwartet 1-basiert
    }

    try:
        r = requests.get(BASE_URL, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()

        if not data.get("results"):
            logger.warning(f"[NewsAPI] Keine Artikel für {category} ({language})")
            return []

        articles = []
        for item in data["results"]:
            articles.append({
                "title": item.get("title", ""),
                "description": item.get("description", ""),
                "url": item.get("link", ""),
                "source": item.get("source_id", ""),
                "published_at": item.get("pubDate", "")
            })

        logger.info(f"[NewsAPI] {len(articles)} Artikel erhalten für {category} ({language})")
        return articles

    except requests.exceptions.RequestException as e:
        logger.error(f"[NewsAPI] Fehler beim Abruf: {e}")
        return []


def compute_importance(article):
    """Berechnet eine einfache Wichtigkeit."""
    text = (article.get("title", "") or "") + " " + (article.get("description", "") or "")
    score = 0
    if "breaking" in text.lower():
        score += 2
    if "exclusive" in text.lower():
        score += 1
    if len(text) > 200:
        score += 0.5
    return score
