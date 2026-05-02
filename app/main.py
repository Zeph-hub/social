from fastapi import FastAPI, BackgroundTasks
from sqlalchemy import text
from app.db.session import SessionLocal
from app.services.pipeline import run_pipeline
from app.api.routes.ingestion import router as ingestion_router
from app.api.routes.analytics import router as analytics_router
from app.api.routes.processed import router as processed_router
from app.core.logging import configure_logging

configure_logging()

app = FastAPI(title="Social Analytics Platform", version="0.1.0")
app.include_router(ingestion_router, prefix="/api/ingestion", tags=["ingestion"])
app.include_router(analytics_router, prefix="/api/analytics", tags=["analytics"])
app.include_router(processed_router, prefix="/api/processed", tags=["processed"])

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

