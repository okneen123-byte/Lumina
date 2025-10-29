# backend/auth.py
import sqlite3
from passlib.hash import bcrypt
from datetime import datetime
from config import DB_PATH
import logging

logger = logging.getLogger("auth")
if not logger.handlers:
    h = logging.StreamHandler()
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    h.setFormatter(fmt)
    logger.addHandler(h)
logger.setLevel(logging.INFO)

MAX_BCRYPT_BYTES = 72  # bcrypt limit

def _sanitize_password(pw):
    """Sicherstellen, dass pw ein str ist, führende/abschließende WS entfernen.
    Rückgabe: (clean_pw, byte_length)"""
    if pw is None:
        return "", 0
    if not isinstance(pw, str):
        # Falls Bytes oder anderes Objekt kommt, versuchen string-convert
        try:
            pw = str(pw)
        except Exception:
            pw = ""
    # Entferne unsichtbare NBSP / zero-width (optional)
    # pw = pw.replace("\u00A0", " ")
    # pw = pw.replace("\u200B", "")
    clean = pw.strip()
    blen = len(clean.encode("utf-8"))
    return clean, blen

def create_user(email: str, password: str):
    """Erstellt einen neuen Nutzer mit gehashtem Passwort."""
    pw, blen = _sanitize_password(password)
    logger.info(f"[auth] create_user called for {email!r} pw_repr={repr(pw)} bytes={blen}")
    if blen == 0:
        raise ValueError("Password must not be empty.")
    if blen > MAX_BCRYPT_BYTES:
        raise ValueError("Password too long: max 72 bytes allowed.")
    pw_hash = bcrypt.hash(pw)
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
    except sqlite3.IntegrityError:
        conn.close()
        return False
    conn.close()
    return True

def verify_user(email: str, password: str):
    """Überprüft E-Mail + Passwort, gibt True/False zurück."""
    pw, blen = _sanitize_password(password)
    logger.info(f"[auth] verify_user called for {email!r} pw_repr={repr(pw)} bytes={blen}")
    if blen == 0 or blen > MAX_BCRYPT_BYTES:
        # zu kurz/leer oder zu lang -> sofort False (kein 500)
        return False

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE email=?", (email,))
    row = c.fetchone()
    conn.close()
    if not row:
        return False
    pw_hash = row[0]
    try:
        return bcrypt.verify(pw, pw_hash)
    except ValueError as e:
        # z. B. wenn pw_hash ein unerwarteter Wert ist
        logger.exception("[auth] bcrypt.verify failed: %s", e)
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
