# backend/news_api.py
import requests
import os
import logging

# Hole API-Key aus Umgebungsvariable (Render Secret)
NEWS_API_KEY = os.getenv("NEWSDATA_API_KEY")

logger = logging.getLogger("news_api")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)


def fetch_news_from_api(category="general", language="en", page_size=40):
    """Holt News von NewsData.io API."""
    try:
        if not NEWS_API_KEY:
            logger.error("❌ Kein NEWS_API_KEY gefunden (Secret fehlt!)")
            return []

        url = (
            f"https://newsdata.io/api/1/news?"
            f"category={category}&language={language}&size={page_size}&apikey={NEWS_API_KEY}"
        )

        response = requests.get(url)
        if response.status_code != 200:
            logger.error(f"API Fehler {response.status_code}: {response.text}")
            return []

        data = response.json()
        articles = []
        for item in data.get("results", []):
            articles.append({
                "title": item.get("title", ""),
                "description": item.get("description", ""),
                "url": item.get("link", ""),
                "source": item.get("source_id", ""),
                "published_at": item.get("pubDate", ""),
            })
        return articles

    except Exception as e:
        logger.exception("Fehler bei fetch_news_from_api: %s", e)
        return []


def compute_importance(article):
    """Berechnet grob, wie wichtig ein Artikel ist."""
    score = 0
    if article.get("title"):
        score += len(article["title"]) / 10
    if article.get("description"):
        score += len(article["description"]) / 20
    if "breaking" in (article.get("title", "") + article.get("description", "")).lower():
        score += 10
    return score

