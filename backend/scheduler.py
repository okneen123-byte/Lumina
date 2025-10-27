# bac# backend/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from backend.database import save_news_for_category
from config import UPDATE_INTERVAL_HOURS
import time
import traceback

CATEGORIES = ["general", "technology", "business", "sports", "science", "entertainment"]
LANGUAGES = ["en", "de"]  # Englisch + Deutsch

def update_all():
    """Lädt News für alle Kategorien und Sprachen."""
    print("[Scheduler] Starte News-Aktualisierung...")
    for lang in LANGUAGES:
        for cat in CATEGORIES:
            try:
                save_news_for_category(category=cat, language=lang)
                print(f"[Scheduler] ✅ Gespeichert: {cat} ({lang})")
            except Exception as e:
                print(f"[Scheduler] ❌ Fehler beim Speichern {cat} ({lang}): {e}")
                traceback.print_exc()
    print("[Scheduler] ✅ Aktualisierung abgeschlossen.\n")

_scheduler = None

def start_scheduler():
    """Startet den automatischen Scheduler (alle X Stunden)."""
    global _scheduler
    if _scheduler is None:
        _scheduler = BackgroundScheduler()
        _scheduler.add_job(update_all, "interval", hours=UPDATE_INTERVAL_HOURS)
        _scheduler.start()
        print(f"[Scheduler] gestartet – alle {UPDATE_INTERVAL_HOURS} Stunden.")

        # Direkt beim Start einmal ausführen:
        try:
            update_all()
        except Exception as e:
            print(f"[Scheduler] Erster Start fehlgeschlagen: {e}")
