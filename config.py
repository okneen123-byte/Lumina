# config.py
# ========== Füge hier deine echten Keys ein ==========

# NewsAPI (https://newsapi.org) - Key (Test/Prod)
NEWS_API_KEY = "DEIN_NEWSAPI_KEY_HIER"

# Scheduler: Stunden zwischen Updates
UPDATE_INTERVAL_HOURS = 4  # 4 Stunden wie gewünscht

# Free Trial Limit (pro Tag)
FREE_TRIAL_LIMIT = 10

# Optional: Stripe - falls du später Zahlungen integrieren willst
STRIPE_SECRET_KEY = "sk_test_DEIN_KEY"
STRIPE_PUBLISHABLE_KEY = "pk_test_DEIN_KEY"
PAID_PLAN_PRICE_ID = "price_123456789"

# DB Pfad (relativ zum Projekt)
DB_PATH = "backend/news.db"