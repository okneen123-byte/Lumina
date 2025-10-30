# backend/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from backend.database import save_news_for_category
from config import UPDATE_INTERVAL_HOURS, CATEGORIES, LANGUAGES

def update_all():
    print("[Scheduler] Starte News-Aktualisierung...")
    for lang in LANGUAGES:
        for cat in CATEGORIES:
            try:
                save_news_for_category(cat, lang)
                print(f"[Scheduler] ✅ Gespeichert: {cat} ({lang})")
            except Exception as e:
                print(f"[Scheduler] ❌ Fehler bei {cat} ({lang}): {e}")
    print("[Scheduler] ✅ Aktualisierung abgeschlossen.")

_scheduler = None
def start_scheduler():
    global _scheduler
    if _scheduler is None:
        _scheduler = BackgroundScheduler()
        _scheduler.add_job(update_all, "interval", hours=UPDATE_INTERVAL_HOURS)
        _scheduler.start()
        print(f"[Scheduler] gestartet – alle {UPDATE_INTERVAL_HOURS} Stunden.")
