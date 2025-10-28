# backend/news_api.py
import os
import requests
from datetime import datetime

# NewsDataAPI Key aus Environment Secret
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

if not NEWS_API_KEY:
    raise RuntimeError("NEWS_API_KEY nicht gesetzt! Bitte als Secret bei Render hinzufügen.")

def fetch_news_from_api(category="general", language="en", page_size=40):
    """
    Ruft News von NewsDataAPI ab.
    category: 'general', 'technology', 'business', etc.
    language: 'en' oder 'de'
    page_size: Anzahl Artikel
    """
    url = (
        f"https://newsdata.io/api/1/news?"
        f"apikey={NEWS_API_KEY}&language={language}&category={category}&page={1}"
    )

    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        articles = []
        for a in data.get("results", []):
            articles.append({
                "title": a.get("title", ""),
                "description": a.get("description", ""),
                "url": a.get("link", ""),
                "source": a.get("source_id", ""),
                "published_at": a.get("pubDate", datetime.utcnow().isoformat())
            })

        return articles[:page_size]

    except Exception as e:
        print(f"[NewsAPI] Fehler beim Abrufen der News: {e}")
        return []

def compute_importance(article: dict) -> float:
    """
    Dummy-Berechnung der Wichtigkeit.
    Du kannst hier beliebige Logik einfügen.
    """
    score = 0.0
    if article.get("title"):
        score += 1.0
    if article.get("description"):
        score += 0.5
    return score
