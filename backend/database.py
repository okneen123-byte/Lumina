# backend/database.py
import sqlite3
from config import DB_PATH
from backend.news_api import fetch_news_from_api, compute_importance
from datetime import datetime, date

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # News table
    c.execute("""
    CREATE TABLE IF NOT EXISTS news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        title TEXT,
        description TEXT,
        url TEXT UNIQUE,
        source TEXT,
        published_at TEXT,
        importance REAL,
        language TEXT,
        saved_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    # user_queries (for free trial)
    c.execute("""
    CREATE TABLE IF NOT EXISTS user_queries (
        email TEXT,
        date TEXT,
        count INTEGER DEFAULT 0,
        PRIMARY KEY(email, date)
    )
    """)
    # users table is created by auth.create_user if needed
    conn.commit()
    conn.close()

def save_news_for_category(category="general", language="en"):
    articles = fetch_news_from_api(category=category, language=language, page_size=40)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for a in articles:
        importance = compute_importance(a)
        try:
            c.execute("""
                INSERT OR IGNORE INTO news (category, title, description, url, source, published_at, importance, language)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (category, a["title"], a["description"], a["url"], a["source"], a["published_at"], importance, language))
        except Exception:
            # ignore single insert failures
            pass
    conn.commit()
    conn.close()

def get_news(category="general", language="en", sort_by="newest", limit=50):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    order_clause = "ORDER BY datetime(published_at) DESC" if sort_by == "newest" else "ORDER BY importance DESC, datetime(published_at) DESC"
    c.execute(f"SELECT title, description, url, source, published_at, importance FROM news WHERE category=? AND language=? {order_clause} LIMIT ?", (category, language, limit))
    rows = c.fetchall()
    conn.close()
    news = []
    for r in rows:
        news.append({
            "title": r[0],
            "description": r[1],
            "url": r[2],
            "source": r[3],
            "published_at": r[4],
            "importance": float(r[5]) if r[5] is not None else 0.0
        })
    return news

def increment_user_query(email: str):
    """Zählt Anfragen pro Tag (für Free Trial)."""
    today = date.today().isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT count FROM user_queries WHERE email=? AND date=?", (email, today))
    row = c.fetchone()
    if row:
        new_count = row[0] + 1
        c.execute("UPDATE user_queries SET count=? WHERE email=? AND date=?", (new_count, email, today))
    else:
        new_count = 1
        c.execute("INSERT INTO user_queries (email, date, count) VALUES (?, ?, ?)", (email, today, new_count))
    conn.commit()
    conn.close()
    return new_count

def get_user_query_count_today(email: str):
    today = date.today().isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT count FROM user_queries WHERE email=? AND date=?", (email, today))
    row = c.fetchone()
    conn.close()
    return row[0] if row else 0
