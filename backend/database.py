# backend/database.py
import sqlite3
import logging
from datetime import date
from config import DB_PATH
from backend.news_api import fetch_news_from_api, compute_importance

# Logging
logger = logging.getLogger("database")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

# DB-Verbindung
def _get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# Initialisierung
def init_db():
    """Erstellt Tabellen, falls sie fehlen"""
    try:
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
                PRIMARY KEY(email, date)
            )
        """)
        conn.commit()
        logger.info("Datenbank initialisiert.")
    except Exception as e:
        logger.exception(f"DB-Init Fehler: {e}")
    finally:
        conn.close()

# News speichern
def save_news_for_category(category="general", language="en"):
    try:
        articles = fetch_news_from_api(category, language)
        if not articles:
            logger.info(f"Keine News für Kategorie '{category}'")
            return
        conn = _get_conn()
        c = conn.cursor()
        for a in articles:
            importance = compute_importance(a)
            try:
                c.execute("""
                    INSERT OR IGNORE INTO news
                    (category, title, description, url, source, published_at, importance, language)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    category, a["title"], a["description"], a["url"],
                    a["source"], a["published_at"], importance, language
                ))
            except Exception as e:
                logger.warning(f"Artikel Insert Fehler: {e}")
        conn.commit()
        logger.info(f"{len(articles)} News für '{category}' gespeichert.")
    except Exception as e:
        logger.exception(f"save_news Fehler: {e}")
    finally:
        try:
            conn.close()
        except:
            pass

# News abrufen
def get_news(category="general", language="en", sort_by="newest", limit=50):
    news = []
    try:
        conn = _get_conn()
        c = conn.cursor()
        order = "ORDER BY datetime(published_at) DESC" if sort_by=="newest" else "ORDER BY importance DESC, datetime(published_at) DESC"
        c.execute(f"""
            SELECT title, description, url, source, published_at, importance
            FROM news WHERE category=? AND language=? {order} LIMIT ?
        """, (category, language, limit))
        rows = c.fetchall()
        for r in rows:
            news.append({
                "title": r[0],
                "description": r[1],
                "url": r[2],
                "source": r[3],
                "published_at": r[4],
                "importance": float(r[5]) if r[5] else 0
            })
    except Exception as e:
        logger.exception(f"get_news Fehler: {e}")
    finally:
        try: conn.close()
        except: pass
    return news

# Free-Trial Counter
def increment_user_query(email: str):
    today = date.today().isoformat()
    count = 0
    try:
        conn = _get_conn()
        c = conn.cursor()
        c.execute("SELECT count FROM user_queries WHERE email=? AND date=?", (email, today))
        row = c.fetchone()
        if row:
            count = row[0]+1
            c.execute("UPDATE user_queries SET count=? WHERE email=? AND date=?", (count,email,today))
        else:
            count = 1
            c.execute("INSERT INTO user_queries (email,date,count) VALUES (?,?,?)",(email,today,count))
        conn.commit()
    except Exception as e:
        logger.exception(f"increment_user_query Fehler: {e}")
    finally:
        try: conn.close()
        except: pass
    return count

def get_user_query_count_today(email: str):
    today = date.today().isoformat()
    count = 0
    try:
        conn = _get_conn()
        c = conn.cursor()
        c.execute("SELECT count FROM user_queries WHERE email=? AND date=?", (email,today))
        row = c.fetchone()
        if row:
            count = row[0]
    except Exception as e:
        logger.exception(f"get_user_query_count_today Fehler: {e}")
    finally:
        try: conn.close()
        except: pass
    return count
