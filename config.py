# config.py
# ========== Lumina News KI Configuration ==========

# Dein NewsData.io API Key
NEWS_API_KEY = "pub_61224dd3e7214d59b44bf40b85f1858f"

# Scheduler-Intervall (Stunden)
UPDATE_INTERVAL_HOURS = 12  # 2x pro Tag

# Kostenloses Limit (pro Tag)
FREE_TRIAL_LIMIT = 10

# Pfad zur SQLite-Datenbank
DB_PATH = "backend/news.db"

# Kategorien (inkl. Powi)
CATEGORIES = ["general", "technology", "business", "sports", "science", "entertainment", "powi"]
LANGUAGES = ["en", "de"]
