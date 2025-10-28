# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.database import (
    init_db, get_news, get_personalized_news,
    increment_user_query, get_user_query_count_today
)
from backend.scheduler import start_scheduler
from backend.auth import create_user, verify_user, is_paid
from backend.personalization import set_user_preferences, init_preferences_table
from config import FREE_TRIAL_LIMIT

# Init FastAPI
app = FastAPI(title="Lumina KI News API")

# Models
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
    language: str = "en"
    sort_by: str = "newest"
    limit: int = 30

# Initialisierung
init_db()
init_preferences_table()
start_scheduler()

# Auth
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

# News Endpoints
@app.post("/news")
def news(req: NewsRequest):
    email = req.email.lower()
    if not verify_user(email, req.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not is_paid(email):
        count = increment_user_query(email)
        if count > FREE_TRIAL_LIMIT:
            raise HTTPException(status_code=403, detail="Free trial limit reached.")

    limit = max(5, min(100, req.limit))
    results = get_news(req.category, req.language, req.sort_by, limit)
    return {"category": req.category, "news": results}

# Interessen speichern
@app.post("/set_preferences")
def set_preferences(data: dict):
    email = data.get("email")
    interests = data.get("interests")
    if not email or not interests:
        raise HTTPException(status_code=400, detail="Email und Interessen erforderlich.")
    if set_user_preferences(email, interests):
        return {"status": "ok", "message": f"Interessen gespeichert: {interests}"}
    raise HTTPException(status_code=500, detail="Fehler beim Speichern.")

# Personalisierte News
@app.post("/news/personalized")
def personalized_news(data: dict):
    email = data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email erforderlich.")
    news = get_personalized_news(email)
    if not news:
        raise HTTPException(status_code=404, detail="Keine personalisierten News gefunden.")
    return {"email": email, "personalized_news": news}

