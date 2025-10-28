# backend/personalization.py
import sqlite3
from config import DB_PATH
import logging
import re
from difflib import SequenceMatcher

logger = logging.getLogger("personalization")

# Verbindung zur Datenbank
def _get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# Tabelle für Nutzerinteressen erstellen
def init_preferences_table():
    try:
        conn = _get_conn()
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                email TEXT PRIMARY KEY,
                interests TEXT
            )
        """)
        conn.commit()
        logger.info("Tabelle 'user_preferences' erfolgreich initialisiert.")
    except Exception as e:
        logger.exception("Fehler beim Erstellen der Tabelle user_preferences: %s", e)
    finally:
        conn.close()

# Interessen speichern oder aktualisieren
def set_user_preferences(email: str, interests: str):
    try:
        conn = _get_conn()
        c = conn.cursor()
        c.execute("""
            INSERT INTO user_preferences (email, interests)
            VALUES (?, ?)
            ON CONFLICT(email) DO UPDATE SET interests=excluded.interests
        """, (email.lower(), interests.lower()))
        conn.commit()
        logger.info(f"Interessen für {email} gespeichert: {interests}")
        return True
    except Exception as e:
        logger.exception("Fehler beim Speichern der Interessen: %s", e)
        return False
    finally:
        conn.close()

# Interessen abrufen
def get_user_preferences(email: str):
    try:
        conn = _get_conn()
        c = conn.cursor()
        c.execute("SELECT interests FROM user_preferences WHERE email=?", (email.lower(),))
        row = c.fetchone()
        if row:
            return row[0]
    except Exception as e:
        logger.exception("Fehler beim Abrufen der Interessen: %s", e)
    finally:
        conn.close()
    return None

# Einfache KI-basierte Relevanzanalyse
def compute_relevance_score(article_title, article_description, user_interests):
    text = f"{article_title} {article_description}".lower()
    words = re.findall(r"\w+", user_interests.lower())
    score = 0
    for w in words:
        score += SequenceMatcher(None, w, text).ratio()
    return round(score / len(words), 3) if words else 0
