# backend/auth.py
import sqlite3
from passlib.hash import bcrypt
from datetime import datetime
from config import DB_PATH

def create_user(email: str, password: str):
    """Erstellt einen neuen Nutzer mit gehashtem Passwort."""
    # Passwort prüfen (nicht leer & max. 72 Zeichen)
    if not password or len(password.encode("utf-8")) > 72:
        raise ValueError("Password must be 1–72 characters long.")

    # Passwort hashen
    pw_hash = bcrypt.hash(password)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Tabelle erstellen, falls sie noch nicht existiert
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password_hash TEXT,
            is_paid INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)

    try:
        c.execute(
            "INSERT INTO users (email, password_hash, created_at) VALUES (?, ?, ?)",
            (email, pw_hash, datetime.utcnow().isoformat())
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return False  # Benutzer existiert bereits

    conn.close()
    return True


def verify_user(email: str, password: str):
    """Überprüft E-Mail + Passwort, gibt True/False zurück."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE email=?", (email,))
    row = c.fetchone()
    conn.close()

    if not row:
        return False

    pw_hash = row[0]
    try:
        return bcrypt.verify(password, pw_hash)
    except ValueError:
        # Falls Passwort zu lang ist oder Formatfehler entsteht
        return False


def set_paid(email: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET is_paid=1 WHERE email=?", (email,))
    conn.commit()
    conn.close()


def is_paid(email: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT is_paid FROM users WHERE email=?", (email,))
    row = c.fetchone()
    conn.close()
    if not row:
        return False
    return bool(row[0])

