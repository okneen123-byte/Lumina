# backend/database.py
import sqlite3
from config import DB_PATH
from backend.news_api import fetch_news_from_api, compute_importance
from datetime import datetime, date
import logging

# Logging für Render-Debug
logger = logging.getLogger("database")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)


def _get_conn():
    """SQLite Verbindung, check_same_thread=False für Render/uvicorn kompatibel."""
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    """Initialisiert alle Tabellen."""
    try:
        conn = _get_conn()
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
        # user_queries table für Free Trial
        c.execute("""
        CREATE TABLE IF NOT EXISTS user_queries (
            email TEXT,
            date TEXT,
            count INTEGER DEFAULT 0,
            PRIMARY KEY(email, date)
        )
        """)
        conn.commit()
    except Exception as e:
        logger.exception("Fehler beim Initialisieren der DB: %s", e)
    finally:
        conn.close()


def save_news_for_category(category="general", language="en"):
    """Speichert News-Artikel aus der API in der DB."""
    articles = fetch_news_from_api(category=category, language=language, page_size=40)
    try:
        conn = _get_conn()
        c = conn.cursor()
        for a in articles:
            importance = compute_importance(a)
            try:
                c.execute("""
                    INSERT OR IGNORE INTO news (category, title, description, url, source, published_at, importance, language)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (category, a.get("title",""), a.get("description",""), a.get("url",""),
                      a.get("source",""), a.get("published_at",""), importance, language))
            except Exception as e:
                logger.warning("Fehler beim Einfügen eines Artikels: %s", e)
        conn.commit()
    except Exception as e:
        logger.exception("save_news_for_category DB-Fehler: %s", e)
    finally:
        conn.close()


def get_news(category="general", language="en", sort_by="newest", limit=50):
    """Gibt eine Liste von News zurück."""
    news = []
    try:
        conn = _get_conn()
        c = conn.cursor()
        order_clause = "ORDER BY datetime(published_at) DESC" if sort_by == "newest" else "ORDER BY importance DESC, datetime(published_at) DESC"
        c.execute(f"""
            SELECT title, description, url, source, published_at, importance
            FROM news
            WHERE category=? AND language=?
            {order_clause}
            LIMIT ?
        """, (category, language, limit))
        rows = c.fetchall()
        for r in rows:
            news.append({
                "title": r[0],
                "description": r[1],
                "url": r[2],
                "source": r[3],
                "published_at": r[4],
                "importance": float(r[5]) if r[5] is not None else 0.0
            })
    except Exception as e:
        logger.exception("get_news DB-Fehler: %s", e)
    finally:
        conn.close()
    return news


def increment_user_query(email: str):
    """Zählt Anfragen pro Tag (Free Trial)."""
    today = date.today().isoformat()
    count = 0
    try:
        conn = _get_conn()
        c = conn.cursor()
        c.execute("SELECT count FROM user_queries WHERE email=? AND date=?", (email, today))
        row = c.fetchone()
        if row:
            count = row[0] + 1
            c.execute("UPDATE user_queries SET count=? WHERE email=? AND date=?", (count, email, today))
        else:
            count = 1
            c.execute("INSERT INTO user_queries (email, date, count) VALUES (?, ?, ?)", (email, today, count))
        conn.commit()
    except Exception as e:
        logger.exception("increment_user_query DB-Fehler: %s", e)
    finally:
        conn.close()
    return count


def get_user_query_count_today(email: str):
    """Gibt die Anzahl der Anfragen des Nutzers heute zurück."""
    today = date.today().isoformat()
    count = 0
    try:
        conn = _get_conn()
        c = conn.cursor()
        c.execute("SELECT count FROM user_queries WHERE email=? AND date=?", (email, today))
        row = c.fetchone()
        if row:
            count = row[0]
    except Exception as e:
        logger.exception("get_user_query_count_today DB-Fehler: %s", e)
    finally:
        conn.close()
    return count
