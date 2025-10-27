# backend/auth.py
import sqlite3
import re
import logging
from datetime import datetime
from passlib.hash import pbkdf2_sha256
from config import DB_PATH

# Logging (schreibt in Render-Logs)
logger = logging.getLogger("auth")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)


EMAIL_RE = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


def _get_conn():
    """
    Liefert eine SQLite-Verbindung. check_same_thread=False hilft in
    manchen Deploy-Umgebungen mit Threading/Pool (Render/uvicorn).
    """
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def _ensure_tables():
    """Erstellt die users-Tabelle, falls noch nicht vorhanden."""
    conn = _get_conn()
    try:
        with conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    email TEXT PRIMARY KEY,
                    password_hash TEXT NOT NULL,
                    is_paid INTEGER DEFAULT 0,
                    created_at TEXT
                )
                """
            )
    finally:
        conn.close()


# sicherstellen, dass Tabelle existiert beim Modul-Import
try:
    _ensure_tables()
except Exception as e:
    logger.exception("Fehler beim Erstellen/Prüfen der DB-Tabellen: %s", e)


def create_user(email: str, password: str) -> bool:
    """
    Erstellt einen neuen Nutzer mit gehashtem Passwort.
    Gibt True zurück bei Erfolg, False wenn der Nutzer schon existiert oder ein Fehler auftrat.
    Validierung:
      - email muss ein plausibles Format haben
      - password muss nicht leer sein (Länge >= 1)
    Hinweis: wir verwenden pbkdf2_sha256 (kein natives bcrypt-Backend erforderlich).
    """
    if not email or not EMAIL_RE.match(email):
        logger.info("create_user: ungültige E-Mail: %r", email)
        return False

    if not password or not isinstance(password, str) or len(password) == 0:
        logger.info("create_user: ungültiges Passwort (leer).")
        return False

    try:
        # Hash erzeugen (pbkdf2_sha256 kümmert sich um Salt & Iterationen)
        pw_hash = pbkdf2_sha256.hash(password)

        conn = _get_conn()
        try:
            with conn:
                conn.execute(
                    "INSERT INTO users (email, password_hash, created_at) VALUES (?, ?, ?)",
                    (email.lower(), pw_hash, datetime.utcnow().isoformat()),
                )
        finally:
            conn.close()
        logger.info("create_user: Benutzer %s erstellt.", email)
        return True
    except sqlite3.IntegrityError:
        # bereits vorhanden
        logger.info("create_user: Benutzer %s existiert bereits.", email)
        return False
    except Exception as e:
        # allgemeiner Fehler — loggen, aber nicht sensitive Daten preisgeben
        logger.exception("create_user: unerwarteter Fehler: %s", e)
        return False


def verify_user(email: str, password: str) -> bool:
    """
    Überprüft E-Mail + Passwort. Gibt True zurück, wenn die Kombination stimmt.
    """
    if not email or not password:
        return False

    try:
        conn = _get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT password_hash FROM users WHERE email = ?", (email.lower(),))
            row = cur.fetchone()
        finally:
            conn.close()

        if not row:
            logger.info("verify_user: Benutzer %s nicht gefunden.", email)
            return False

        pw_hash = row[0]
        try:
            ok = pbkdf2_sha256.verify(password, pw_hash)
            if ok:
                logger.info("verify_user: Auth erfolgreich für %s", email)
            else:
                logger.info("verify_user: Auth fehlgeschlagen für %s", email)
            return ok
        except Exception as e:
            # kann auftreten wenn Hash beschädigt ist
            logger.exception("verify_user: Fehler beim Verifizieren: %s", e)
            return False
    except Exception as e:
        logger.exception("verify_user: DB-Fehler: %s", e)
        return False


def set_paid(email: str) -> bool:
    """Markiert einen Benutzer als bezahlt. Gibt True bei Erfolg zurück."""
    if not email:
        return False
    try:
        conn = _get_conn()
        try:
            with conn:
                cur = conn.execute("UPDATE users SET is_paid = 1 WHERE email = ?", (email.lower(),))
                updated = cur.rowcount
        finally:
            conn.close()
        logger.info("set_paid: %s -> updated %s rows", email, updated)
        return updated > 0
    except Exception as e:
        logger.exception("set_paid: Fehler: %s", e)
        return False


def is_paid(email: str) -> bool:
    """Prüft, ob der Benutzer bezahlt ist."""
    if not email:
        return False
    try:
        conn = _get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT is_paid FROM users WHERE email = ?", (email.lower(),))
            row = cur.fetchone()
        finally:
            conn.close()

        if not row:
            return False
        return bool(row[0])
    except Exception as e:
        logger.exception("is_paid: DB-Fehler: %s", e)
    return False
