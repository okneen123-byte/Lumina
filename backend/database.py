# backend/database.py
import sqlite3
import logging
from datetime import date
from config import DB_PATH
from backend.news_api import fetch_news_from_api, compute_importance

# ------------------- Logging -------------------
logger = logging.getLogger("database")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)


# ------------------- DB-Verbindung -------------------
def _get_conn():
    """Erstellt eine SQLite-Verbindung, kompatibel mit Render/uvicorn."""
    return sqlite3.connect(DB_PATH, check_same_thread=False)


# ------------------- Initialisierung -------------------
def init_db():
    """Erstellt alle benötigten Tabellen, falls sie fehlen."""
    try:
        conn = _get_conn()
        c = conn.cursor()

        # NEWS TABLE
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

        # USER_QUERIES TABLE (für Free Trial)
        c.execute("""
        CREATE TABLE IF NOT EXISTS user_queries (
            email TEXT NOT NULL,
            date TEXT NOT NULL,
            count INTEGER DEFAULT 0,
            PRIMARY KEY (email, date)
        )
        """)

        # USERS TABLE (zur Sicherheit, falls auth es nicht selbst erstellt)
        c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password_hash TEXT,
            is_paid INTEGER DEFAULT 0,
            created_at TEXT
        )
        """)

        conn.commit()
        logger.info("✅ Datenbanktabellen erfolgreich initialisiert.")
    except Exception as e:
        logger.exception("❌ Fehler beim Initialisieren der Datenbank: %s", e)
    finally:
        try:
            conn.close()
        except Exception:
            pass


# ------------------- News speichern -------------------
def save_news_for_category(category="general", language="en"):
    """Lädt News aus der API und speichert sie in der Datenbank."""
    try:
        articles = fetch_news_from_api(category=category, language=language, page_size=40)
        if not articles:
            logger.info(f"ℹ Keine Artikel für Kategorie '{category}' gefunden.")
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
                    a.get("url", ""),
                    a.get("source", ""),
                    a.get("published_at", ""),
                    importance,
                    language
                ))
            except Exception as e:
                logger.warning("⚠ Fehler beim Einfügen eines Artikels: %s", e)

        conn.commit()
        logger.info(f"✅ News für Kategorie '{category}' gespeichert.")
    except Exception as e:
        logger.exception("❌ save_news_for_category DB-Fehler: %s", e)
    finally:
        try:
            conn.close()
        except Exception:
            pass


# ------------------- News abrufen -------------------
def get_news(category="general", language="en", sort_by="newest", limit=50):
    """Holt News aus der Datenbank."""
    news = []
    try:
        conn = _get_conn()
        c = conn.cursor()

        order_clause = (
            "ORDER BY datetime(published_at) DESC"
            if sort_by == "newest"
            else "ORDER BY importance DESC, datetime(published_at) DESC"
        )

        query = f"""
        SELECT title, description, url, source, published_at, importance
        FROM news
        WHERE category=? AND language=?
        {order_clause}
        LIMIT ?
        """
        c.execute(query, (category, language, limit))
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

        logger.info(f"✅ {len(news)} News für Kategorie '{category}' geladen.")
    except Exception as e:
        logger.exception("❌ get_news DB-Fehler: %s", e)
    finally:
        try:
            conn.close()
        except Exception:
            pass

    return news


# ------------------- Free-Trial Counter -------------------
def increment_user_query(email: str):
    """Erhöht den täglichen Anfragezähler des Nutzers."""
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
        logger.info(f"👤 {email}: Query-Count = {count}")
    except Exception as e:
        logger.exception("❌ increment_user_query DB-Fehler: %s", e)
    finally:
        try:
            conn.close()
        except Exception:
            pass

    return count


def get_user_query_count_today(email: str):
    """Gibt zurück, wie viele Anfragen der Nutzer heute gemacht hat."""
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
        logger.exception("❌ get_user_query_count_today DB-Fehler: %s", e)
    finally:
        try:
            conn.close()
        except Exception:
            pass

    return count


# ------------------- Automatische Initialisierung -------------------
if __name__ == "_main_":
    init_db()

