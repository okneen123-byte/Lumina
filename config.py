import sqlite3
from config import DB_PATH

def init_db():
    """Initialisiert oder repariert die Datenbank automatisch."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Tabelle news
    c.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            url TEXT,
            source TEXT,
            category TEXT,
            language TEXT,
            importance REAL DEFAULT 0,
            published_at TEXT
        )
    """)

    # Tabelle user_queries
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_queries (
            email TEXT,
            date TEXT,
            count INTEGER DEFAULT 0,
            PRIMARY KEY (email, date)
        )
    """)

    # Tabelle users
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password_hash TEXT,
            is_paid INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("[DB] Initialisierung abgeschlossen.")
