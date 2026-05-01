from fastapi import APIRouter, FastAPI, BackgroundTasks
from requests import Session
from app.db.session import SessionLocal
from app.services.pipeline import run_pipeline
from app.api.routes import ingestion, analytics
from app.core.logging import configure_logging

app = FastAPI()
@app.post("/ingest")
async def ingest(platform: str, query: str, bg: BackgroundTasks):
    bg.add_task(run_pipeline, platform, query)
    return {"status": "ingestion started"}

router = APIRouter()
@router.get("/sentiment_summary")
async def get_sentiment_summary():
    db: Session = SessionLocal()

    results = db.execute("""SELECT sentiment, count(*) as count
                         FROM posts
                         GROUP BY sentiment""").fetchall()
    return {r[0]: r[1] for r in results}

