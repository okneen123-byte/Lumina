# backend/auth.py
import sqlite3
from passlib.hash import bcrypt
from datetime import datetime
from config import DB_PATH

MAX_BCRYPT_BYTES = 72

def _sanitize_password(pw):
    if pw is None:
        return "", 0
    if not isinstance(pw, str):
        pw = str(pw)
    clean = pw.strip()
    return clean, len(clean.encode("utf-8"))

def create_user(email: str, password: str):
    """Erstellt neuen Nutzer mit sicherem Passwort-Hash."""
    password, blen = _sanitize_password(password)
    if blen == 0:
        raise ValueError("Password cannot be empty.")
    if blen > MAX_BCRYPT_BYTES:
        raise ValueError("Password too long (max 72 bytes).")

    pw_hash = bcrypt.hash(password)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password_hash TEXT,
            is_paid INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)
    try:
        c.execute("INSERT INTO users (email, password_hash, created_at) VALUES (?, ?, ?)",
                  (email, pw_hash, datetime.utcnow().isoformat()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(email: str, password: str):
    """Überprüft Nutzer-Login."""
    password, _ = _sanitize_password(password)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE email=?", (email,))
    row = c.fetchone()
    conn.close()
    return bool(row) and bcrypt.verify(password, row[0])

def is_paid(email: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT is_paid FROM users WHERE email=?", (email,))
    row = c.fetchone()
    conn.close()
    return bool(row and row[0])
