# backend/config.py
import os

# ========== NEWSDATA.IO API KEY ==========
# Du hast den Key angegeben — steht hier für sofortige Nutzung.
# Empfehlung: In Produktion als Environment-Variable speichern.
NEWS_API_KEY = "pub_61224dd3e7214d59b44bf40b85f1858f"

# Scheduler: Stunden zwischen Updates (12 => 2x täglich)
UPDATE_INTERVAL_HOURS = 12

# Free Trial Limit (pro Tag)
FREE_TRIAL_LIMIT = 10

# Optional: Stripe - falls du später Zahlungen integrieren willst
STRIPE_SECRET_KEY = "sk_test_DEIN_KEY"
STRIPE_PUBLISHABLE_KEY = "pk_test_DEIN_KEY"
PAID_PLAN_PRICE_ID = "price_123456789"

# DB Pfad (relativ zum Projekt; bleibt im backend-Ordner)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "news.db")
