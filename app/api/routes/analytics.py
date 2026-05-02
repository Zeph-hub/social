from fastapi import APIRouter
from sqlalchemy import text

from app.db.session import get_session

router = APIRouter()


@router.get("/summary")
async def summary():
    with get_session() as session:
        results = session.execute(text(
            "SELECT sentiment, count(*) AS count FROM posts GROUP BY sentiment"
        )).fetchall()
        return {"sentiment_counts": {row[0]: row[1] for row in results}}


@router.get("/report")
async def powerbi_report():
    with get_session() as session:
        sentiment_results = session.execute(text(
            "SELECT sentiment, count(*) AS count FROM posts GROUP BY sentiment"
        )).fetchall()
        language_results = session.execute(text(
            "SELECT language, count(*) AS count FROM posts GROUP BY language"
        )).fetchall()
        total = session.execute(text("SELECT COUNT(*) FROM posts")).scalar()

    return {
        "total_posts": total,
        "sentiment_counts": {row[0]: row[1] for row in sentiment_results},
        "language_counts": {row[0]: row[1] for row in language_results},
    }
