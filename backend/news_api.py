# backend/news_api.py
import requests
from dateutil import parser as dateparser
from datetime import datetime, timezone
from config import NEWS_API_KEY

# Keywords, die die Wichtigkeit erhöhen
IMPORTANCE_KEYWORDS = [
    "breaking", "urgent", "exclusive", "explosion", "crash", "attack",
    "krieg", "brutal", "katastrophe", "dringend"
]

def fetch_news_from_api(category="general", language="en", page_size=30):
    """
    Holt Artikel von NewsAPI, gibt Liste standardisierter Artikel zurück.
    language: 'en' oder 'de' (NewsAPI unterstützt 'de' für deutsch)
    """
    base = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": NEWS_API_KEY,
        "category": category,
        "language": language,
        "pageSize": page_size,
    }
    resp = requests.get(base, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    articles = data.get("articles", [])
    normalized = []
    for a in articles:
        published = a.get("publishedAt") or a.get("published_at") or None
        try:
            published_dt = dateparser.parse(published) if published else datetime.now(timezone.utc)
        except Exception:
            published_dt = datetime.now(timezone.utc)
        normalized.append({
            "title": a.get("title") or "",
            "description": a.get("description") or "",
            "url": a.get("url") or "",
            "source": (a.get("source") or {}).get("name") or "",
            "published_at": published_dt.isoformat(),
            "language": language
        })
    return normalized

def compute_importance(article):
    """
    Einfacher Heuristik-Score für Wichtigkeit:
    - recency (stärker wenn sehr neu)
    - keyword boost (breaking, urgent,...)
    - source/description length as minor factors
    """
    now = datetime.now(timezone.utc)
    try:
        published = dateparser.parse(article.get("published_at"))
    except Exception:
        published = now
    hours_old = max(0.0, (now - published).total_seconds() / 3600.0)
    # recency_score: 0..1, 1 = brandneu, 0 = sehr alt (>72h)
    recency_score = max(0.0, 1.0 - (hours_old / 72.0))
    title = (article.get("title") or "").lower()
    desc = (article.get("description") or "").lower()
    keyword_bonus = 0.0
    for kw in IMPORTANCE_KEYWORDS:
        if kw in title or kw in desc:
            keyword_bonus += 0.25
    length_bonus = min(0.2, len(desc) / 500.0)
    score = recency_score * 0.7 + keyword_bonus * 0.2 + length_bonus * 0.1
    # normalize to 0..1
    score = max(0.0, min(1.0, score))
    return score
