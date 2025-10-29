# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.database import init_db, get_news, increment_user_query
from backend.scheduler import start_scheduler
from backend.auth import create_user, verify_user, is_paid
from config import FREE_TRIAL_LIMIT

app = FastAPI(title="Lumina News KI API")

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

# Init DB and scheduler
init_db()
start_scheduler()

@app.post("/signup")
def signup(data: SignupModel):
    try:
        ok = create_user(data.email.lower(), data.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
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
    if not verify_user(email, req.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not is_paid(email):
        count = increment_user_query(email)
        if count > FREE_TRIAL_LIMIT:
            raise HTTPException(status_code=403, detail="Free trial limit reached. Upgrade to premium.")
    if req.sort_by not in ("newest", "importance"):
        req.sort_by = "newest"
    limit = max(5, min(100, req.limit))
    results = get_news(category=req.category, language=req.language, sort_by=req.sort_by, limit=limit)
    return {"category": req.category, "language": req.language, "sort_by": req.sort_by, "news": results}
