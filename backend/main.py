# backend/main.py
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.database import (
    init_db,
    get_news,
    increment_user_query,
    get_user_query_count_today
)
from backend.scheduler import start_scheduler
from backend.auth import create_user, verify_user, is_paid
from config import FREE_TRIAL_LIMIT, DB_PATH

# ------------------- Logging Setup -------------------
logger = logging.getLogger("main")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)


# ------------------- FastAPI Setup -------------------
app = FastAPI(title="Lumina News KI API")


# ------------------- Models -------------------
class SignupModel(BaseModel):
    email: str
    password: str


class LoginModel(BaseModel):
    email: str
    password: str


class NewsRequest(BaseModel):
    email: str
    password: str
    category: str = "general"
    language: str = "en"  # 'en' or 'de'
    sort_by: str = "newest"  # or 'importance'
    limit: int = 30


# ------------------- Init DB and Scheduler -------------------
try:
    init_db()
    start_scheduler()
    logger.info("✅ Backend erfolgreich initialisiert.")
except Exception as e:
    logger.exception("❌ Fehler beim Initialisieren des Backends: %s", e)


# ------------------- Routes -------------------
@app.post("/signup")
def signup(data: SignupModel):
    ok = create_user(data.email.lower(), data.password)
    if not ok:
        raise HTTPException(status_code=400, detail="User exists")
    return {"status": "ok", "message": "User created"}


@app.post("/login")
def login(data: LoginModel):
    if verify_user(data.email.lower(), data.password):
        paid = is_paid(data.email.lower())
        return {"status": "ok", "is_paid": paid}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/news")
def news(req: NewsRequest):
    email = req.email.lower()

    # verify credentials
    if not verify_user(email, req.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # check paid / free trial
    if not is_paid(email):
        count = increment_user_query(email)
        if count > FREE_TRIAL_LIMIT:
            raise HTTPException(
                status_code=403,
                detail="Free trial limit reached. Upgrade to premium."
            )

    # get news from DB
    if req.sort_by not in ("newest", "importance"):
        req.sort_by = "newest"

    limit = max(5, min(100, req.limit))
    results = get_news(
        category=req.category,
        language=req.language,
        sort_by=req.sort_by,
        limit=limit
    )

    logger.info(f"📨 News Request für {email}: {len(results)} Ergebnisse.")
    return {
        "category": req.category,
        "language": req.language,
        "sort_by": req.sort_by,
        "news": results
    }

