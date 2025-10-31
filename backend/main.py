# backend/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from backend.demo_data import DEMO_NEWS
from config import UPDATE_INTERVAL_HOURS

app = FastAPI(title="Lumina News KI – Dark Neon Edition")

class NewsRequest(BaseModel):
    category: str = "general"
    language: str = "en"
    sort_by: str = "newest"

@app.get("/")
def home():
    return {"status": "ok", "message": "Lumina News KI Dark Neon Edition läuft!"}

@app.post("/news")
def get_news(req: NewsRequest):
    lang = req.language if req.language in DEMO_NEWS else "en"
    cat = req.category if req.category in DEMO_NEWS[lang] else "general"
    news_list = DEMO_NEWS[lang][cat]

    if req.sort_by == "importance":
        news_list = sorted(news_list, key=lambda x: x["importance"], reverse=True)
    else:
        news_list = sorted(news_list, key=lambda x: x["published_at"], reverse=True)

    return {
        "language": lang,
        "category": cat,
        "update_interval_hours": UPDATE_INTERVAL_HOURS,
        "count": len(news_list),
        "news": news_list
    }
