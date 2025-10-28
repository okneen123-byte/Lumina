import requests
import logging
from config import NEWS_API_KEY  # ← Holt deinen API-Key korrekt aus config.py

# ------------------------------------------------------
# Logging einrichten
# ------------------------------------------------------
logger = logging.getLogger("news_api")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

# ------------------------------------------------------
# News von der NewsAPI abrufen
# ------------------------------------------------------
def fetch_news_from_api(category="general", language="en", page_size=40):
    """Holt Nachrichten von NewsAPI.org."""
    url = (
        f"https://newsapi.org/v2/top-headlines?"
        f"category={category}&language={language}&pageSize={page_size}&apiKey={NEWS_API_KEY}"
    )

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "ok":
            logger.error(f"Fehlerhafte Antwort von NewsAPI: {data}")
            return []

        articles = data.get("articles", [])
        logger.info(f"{len(articles)} Artikel erfolgreich für '{category}' geladen.")

        return [
            {
                "title": a.get("title", ""),
                "description": a.get("description", ""),
                "url": a.get("url", ""),
                "source": a.get("source", {}).get("name", ""),
                "published_at": a.get("publishedAt", ""),
            }
            for a in articles
        ]

    except requests.exceptions.RequestException as e:
        logger.error(f"Fehler beim Abrufen der NewsAPI: {e}")
        return []

# ------------------------------------------------------
# Wichtigkeit (Importance) berechnen
# ------------------------------------------------------
def compute_importance(article):
    """Berechnet, wie wichtig ein Artikel ist (vereinfacht)."""
    score = 0
    title = article.get("title", "") or ""
    desc = article.get("description", "") or ""

    # Länge des Titels & der Beschreibung
    score += len(title) * 0.1
    score += len(desc) * 0.05

    # Bonuspunkte für bestimmte Schlagwörter
    keywords = ["breaking", "update", "exclusive", "important", "alert"]
    for kw in keywords:
        if kw.lower() in title.lower() or kw.lower() in desc.lower():
            score += 10

    return round(score, 2)


