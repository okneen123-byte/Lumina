# backend/news_api.py
import random
from datetime import datetime

def compute_importance(article):
    """
    Berechnet einen Importance-Score für einen Artikel.
    Gibt einen Wert zwischen 0.3 und 1.0 zurück.
    """
    return round(random.uniform(0.3, 1.0), 2)


def fetch_news_from_api(category="general", language="en", page_size=50):
    """
    Liefert News-Artikel.
    Wenn keine echte API verwendet wird oder keine Artikel verfügbar sind,
    werden automatisch simulierte Artikel generiert.
    
    Args:
        category (str): Kategorie der News (z.B. 'general', 'sports').
        language (str): Sprache der News ('en' oder 'de').
        page_size (int): Anzahl Artikel pro Abruf (max 100 empfohlen).
    
    Returns:
        list[dict]: Liste von News-Artikeln mit Feldern title, description, url, source, published_at.
    """
    articles = []

    for i in range(page_size):
        articles.append({
            "title": f"{category.capitalize()} News #{i+1}",
            "description": f"Dies ist ein automatisch generierter Testartikel #{i+1}.",
            "url": f"https://example.com/news/{category}/{i+1}",
            "source": "Simulated Source",
            "published_at": datetime.utcnow().isoformat() + "Z"
        })

    return articles
