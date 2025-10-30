# backend/database.py
import sqlite3
import logging
from datetime import date
from config import DB_PATH
from backend.news_api import fetch_news_from_api, compute_importance

logger = logging.getLogger("database")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

def _get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = _get_conn()
    c = conn.cursor()

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

    c.execute("""
    CREATE TABLE IF NOT EXISTS user_queries (
        email TEXT NOT NULL,
        date TEXT NOT NULL,
        count INTEGER DEFAULT 0,
        PRIMARY KEY (email, date)
    )
    """)

    conn.commit()
    conn.close()
    logger.info("✅ Datenbank initialisiert.")

def save_news_for_category(category="general", language="en"):
    articles = fetch_news_from_api(category=category, language=language, page_size=40)
    if not articles:
        logger.info(f"Keine Artikel für {category} ({language})")
        return

    conn = _get_conn()
    c = conn.cursor()
    for a in articles:
        try:
            importance = compute_importance(a)
            c.execute("""
                INSERT OR IGNORE INTO news
                (category, title, description, url, source, published_at, importance, language)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                category,
                a.get("title", ""),
                a.get("description", ""),
                a.get("link", ""),
                a.get("source_id", ""),
                a.get("pubDate", ""),
                importance,
                language
            ))
        except Exception as e:
            logger.warning(f"Fehler beim Einfügen: {e}")
    conn.commit()
    conn.close()
    logger.info(f"✅ {category} ({language}) gespeichert.")

def get_news(category="general", language="en", sort_by="newest", limit=50):
    conn = _get_conn()
    c = conn.cursor()
    order = "datetime(published_at) DESC" if sort_by == "newest" else "importance DESC"
    c.execute(f"""
        SELECT title, description, url, source, published_at, importance
        FROM news WHERE category=? AND language=?
        ORDER BY {order} LIMIT ?
    """, (category, language, limit))
    rows = c.fetchall()
    conn.close()
    return [
        {"title": r[0], "description": r[1], "url": r[2], "source": r[3],
         "published_at": r[4], "importance": r[5]} for r in rows
    ]

def increment_user_query(email: str):
    today = date.today().isoformat()
    conn = _get_conn()
    c = conn.cursor()
    c.execute("SELECT count FROM user_queries WHERE email=? AND date=?", (email, today))
    row = c.fetchone()
    count = (row[0] + 1) if row else 1
    if row:
        c.execute("UPDATE user_queries SET count=? WHERE email=? AND date=?", (count, email, today))
    else:
        c.execute("INSERT INTO user_queries (email, date, count) VALUES (?, ?, ?)", (email, today, count))
    conn.commit()
    conn.close()
    return count
