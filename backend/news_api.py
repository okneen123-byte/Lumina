# backend/news_api.py
import requests
import logging
from config import NEWS_API_KEY

logger = logging.getLogger("news_api")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)


def fetch_news_from_api(category="general", language="en", page_size=20):
    """Lädt News von NewsAPI, liefert bei Free-Key-Limit Fallback-Artikel."""
    url = (
        f"https://newsapi.org/v2/top-headlines?"
        f"country=us&category={category}&pageSize={page_size}&apiKey={NEWS_API_KEY}"
    )
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        articles = data.get("articles", [])
        if not articles:
            logger.info("Keine echten Artikel von API erhalten, Fallback wird genutzt.")
            articles = [{
                "title": "Test News",
                "description": "Dies ist ein Testartikel, da Free-Key keine News liefert.",
                "url": "https://example.com/test",
                "source": "Test Source",
                "published_at": "2025-10-28T12:00:00Z"
            }]
        else:
            logger.info(f"{len(articles)} Artikel von NewsAPI geladen.")
        return articles
    except Exception as e:
        logger.exception("Fehler beim Laden von NewsAPI, Fallback wird genutzt: %s", e)
        return [{
            "title": "Test News",
            "description": "API Request fehlgeschlagen, Testartikel.",
            "url": "https://example.com/test",
            "source": "Test Source",
            "published_at": "2025-10-28T12:00:00Z"
        }]


def compute_importance(article):
    """Berechnet Wichtigkeit basierend auf Titel- und Beschreibungslänge."""
    score = 0
    title = article.get("title") or ""
    description = article.get("description") or ""
    score += len(title) / 50  # kurze Titel = kleiner Score
    score += len(description) / 200  # kurze Beschreibung = kleiner Score
    return round(score, 2)
