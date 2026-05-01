from fastapi import FastAPI, BackgroundTasks
from sqlalchemy import text
from app.db.session import SessionLocal
from app.services.pipeline import run_pipeline
from app.core.logging import configure_logging

configure_logging()

app = FastAPI(title="Social Analytics Platform", version="0.1.0")

@app.post("/ingest")
async def ingest(platform: str, query: str, bg: BackgroundTasks):
    bg.add_task(run_pipeline, platform, query)
    return {"status": "ingestion started"}

@app.get("/sentiment_summary")
async def get_sentiment_summary():
    db = SessionLocal()
    try:
        results = db.execute(text("SELECT sentiment, count(*) as count FROM posts GROUP BY sentiment")).fetchall()
        return {r[0]: r[1] for r in results}
    finally:
        db.close()

