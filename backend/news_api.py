# backend/news_api.py
from newsdataapi import NewsDataAPIClient

# API-Key
NEWS_API_KEY = "pub_61224dd3e7214d59b44bf40b85f1858f"
api = NewsDataAPIClient(apikey=NEWS_API_KEY)

def fetch_news_from_api(query="general", language="en", page_size=20):
    """
    Ruft die neuesten Nachrichten von NewsData.io ab.
    """
    try:
        response = api.news_api(q=query, language=language, page_size=page_size)
        articles = response.get("articles", [])
        if not articles:
            return []
        return articles
    except Exception as e:
        print(f"Fehler beim Abrufen der News: {e}")
        return []

def compute_importance(article):
    """
    Optional: Berechnet die Wichtigkeit eines Artikels.
    Beispiel: Je länger der Titel, desto wichtiger.
    """
    title = article.get("title", "")
    return min(len(title) / 50.0, 1.0)
