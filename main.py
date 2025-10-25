# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.database import init_db, get_news, increment_user_query, get_user_query_count_today
from backend.scheduler import start_scheduler
from backend.auth import create_user, verify_user, is_paid
from config import FREE_TRIAL_LIMIT, DB_PATH
from backend.database import init_db as db_init

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
    language: str = "en"  # 'en' or 'de'
    sort_by: str = "newest"  # or 'importance'
    limit: int = 30

app = FastAPI(title="Lumina News KI API")

# Init DB and scheduler
db_init()
start_scheduler()

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
    # Check paid
    if not is_paid(email):
        # increment and check free limit
        count = increment_user_query(email)
        if count > FREE_TRIAL_LIMIT:
            raise HTTPException(status_code=403, detail="Free trial limit reached. Upgrade to premium.")
    # get news from DB
    if req.sort_by not in ("newest", "importance"):
        req.sort_by = "newest"
    # limit sanity
    limit = max(5, min(100, req.limit))
    results = get_news(category=req.category, language=req.language, sort_by=req.sort_by, limit=limit)
    return {"category": req.category, "language": req.language, "sort_by": req.sort_by, "news": results}