# backend/news_api.py
import requests
from config import NEWS_API_KEY
from datetime import datetime

def compute_importance(article):
    """
    Ein einfacher Importance-Wert: 0.5 = Standard.
    Du kannst hier eine KI-Bewertung oder Keyword-Scoring einfügen.
    """
    return 0.5

def fetch_news_from_api(category="general", language="en", page_size=20):
    """
    Ruft News von NewsAPI ab. Falls leer, wird ein Fallback-Artikel zurückgegeben.
    """
    articles = []

    # API URL für Top-Headlines
    url = (
        f"https://newsapi.org/v2/top-headlines?"
        f"language={language}&category={category}&pageSize={page_size}&apiKey={NEWS_API_KEY}"
    )

    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])
    except Exception as e:
        print(f"[NewsAPI] Fehler beim Abrufen: {e}")

    # Fallback-Artikel, falls API leer oder Fehler
    if not articles:
        articles = [
            {
                "title": "Willkommensartikel",
                "description": "Testartikel, damit die App sofort News anzeigt.",
                "url": "https://example.com/news1",
                "source": "Test Source",
                "published_at": datetime.utcnow().isoformat() + "Z"
            },
            {
                "title": "Zweiter Testartikel",
                "description": "Noch ein Artikel für die KI News.",
                "url": "https://example.com/news2",
                "source": "Test Source",
                "published_at": datetime.utcnow().isoformat() + "Z"
            },
            {
                "title": "Dritter Testartikel",
                "description": "Ein weiterer Fallback-Artikel für die Anzeige.",
                "url": "https://example.com/news3",
                "source": "Test Source",
                "published_at": datetime.utcnow().isoformat() + "Z"
            }
        ]

    return articles
