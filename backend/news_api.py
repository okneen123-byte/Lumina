# backend/news_api.py
import requests
from config import NEWS_API_KEY

BASE_URL = "https://newsdata.io/api/1/news"

def fetch_news_from_api(category="general", language="en", page_size=30):
    params = {
        "apikey": NEWS_API_KEY,
        "language": language,
        "category": category if category != "powi" else "politics",
        "page": 0
    }
    try:
        r = requests.get(BASE_URL, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
        return data.get("results", [])
    except Exception as e:
        print(f"[NewsAPI] Fehler beim Abruf: {e}")
        return []

def compute_importance(article):
    score = 0
    if article.get("title"): score += 1
    if article.get("description"): score += 1
    if article.get("source_id"): score += 0.5
    if "breaking" in str(article).lower(): score += 1
    return min(score / 3.5, 1.0)
