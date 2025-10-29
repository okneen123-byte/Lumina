# backend/news_api.py
import requests
from dateutil import parser as dateparser
from datetime import datetime, timezone
from config import NEWS_API_KEY

# Kategorien: wir unterstützen diese im Scheduler / Frontend
VALID_CATEGORIES = ["general", "technology", "business", "sports", "science", "entertainment", "poli"]

# Keywords, die Wichtigkeit erhöhen
IMPORTANCE_KEYWORDS = [
    "breaking", "urgent", "exclusive", "explosion", "crash", "attack",
    "krieg", "brutal", "katastrophe", "dringend", "politics", "economy"
]

BASE_URL = "https://newsdata.io/api/1/news"

def fetch_news_from_api(category="general", language="en", page_size=40):
    """
    Holt Artikel von newsdata.io (newsdata.io API).
    Gibt eine Liste von standardisierten Artikel-Dicts zurück.
    """
    params = {
        "apikey": NEWS_API_KEY,
        "language": language,
        "category": category,
        "page": 0
    }
    articles = []
    try:
        resp = requests.get(BASE_URL, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        # newsdata.io liefert 'results' key
        for item in data.get("results", []):
            published = item.get("pubDate") or item.get("pubDateTime") or item.get("publishedAt") or item.get("date")
            try:
                published_dt = dateparser.parse(published) if published else datetime.now(timezone.utc)
            except Exception:
                published_dt = datetime.now(timezone.utc)
            articles.append({
                "title": item.get("title") or "",
                "description": item.get("description") or item.get("content") or "",
                "url": item.get("link") or item.get("url") or "",
                "source": (item.get("source_id") or item.get("source") or ""),
                "published_at": published_dt.isoformat()
            })
        return articles
    except Exception as e:
        print(f"[NewsAPI] Fehler beim Abruf: {e}")
        return []

def compute_importance(article):
    """Einfache Heuristik: recency + keyword boosts + Länge."""
    score = 0.0
    title = (article.get("title") or "").lower()
    desc = (article.get("description") or "").lower()
    # recency
    try:
        published = dateparser.parse(article.get("published_at"))
        hours_old = max(0.0, (datetime.now(timezone.utc) - published).total_seconds() / 3600.0)
    except Exception:
        hours_old = 9999.0
    recency_score = max(0.0, 1.0 - (hours_old / 72.0))  # 0..1 (<=72h higher)
    # keyword bonus
    keyword_bonus = 0.0
    for kw in IMPORTANCE_KEYWORDS:
        if kw in title or kw in desc:
            keyword_bonus += 0.25
    length_bonus = min(0.2, len(desc) / 500.0)
    score = recency_score * 0.7 + keyword_bonus * 0.2 + length_bonus * 0.1
    return max(0.0, min(1.0, score))
