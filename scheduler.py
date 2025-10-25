# backend/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from backend.database import save_news_for_category
from config import UPDATE_INTERVAL_HOURS
import time

CATEGORIES = ["general", "technology", "business", "sports", "science", "entertainment"]
LANGUAGES = ["en", "de"]  # Englisch + Deutsch

def update_all():
    for lang in LANGUAGES:
        for cat in CATEGORIES:
            try:
                save_news_for_category(category=cat, language=lang)
                print(f"[Scheduler] Saved {cat} ({lang})")
            except Exception as e:
                print(f"[Scheduler] Fehler beim Speichern {cat} ({lang}): {e}")

_scheduler = None

def start_scheduler():
    global _scheduler
    if _scheduler is None:
        _scheduler = BackgroundScheduler()
        _scheduler.add_job(update_all, 'interval', hours=UPDATE_INTERVAL_HOURS, next_run_time=None)
        _scheduler.start()
        print("[Scheduler] gestartet, alle", UPDATE_INTERVAL_HOURS, "Stunden")