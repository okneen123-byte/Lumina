# backend/news_api.py
import requests
from config import NEWS_API_KEY
from datetime import datetime

def fetch_news_from_api(query="general", language="en", page_size=40):
    """
    Holt News von NewsData.io (kostenlose API) zurück.
    query: Kategorie oder Schlagwort
    language: 'en' oder 'de'
    page_size: Anzahl Artikel pro Abruf
    """
    url = f"https://newsdata.io/api/1/news?apikey={NEWS_API_KEY}&q={query}&language={language}&page=0"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        articles = []

        for item in data.get("results", []):
            articles.append({
                "title": item.get("title", ""),
                "description": item.get("description", ""),
                "url": item.get("link", ""),
                "source": item.get("source_id", ""),
                "published_at": item.get("pubDate", datetime.utcnow().isoformat())
            })

        return articles
    except Exception as e:
        print("Fehler beim Abrufen der News:", e)
        return []

def compute_importance(article):
    """
    Berechnet Importance Score.
    Momentan simple Dummy-Logik:
    - längere Titel → etwas höher
    """
    if not article.get("title"):
        return 0.0
    score = len(article["title"]) / 100
    return round(score, 2)

