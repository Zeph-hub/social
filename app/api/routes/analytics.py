from fastapi import APIRouter

from app.db.models import SocialRecord
from app.db.session import get_session
from app.services.ml import analyze

router = APIRouter()


@router.get("/summary")
async def summary():
    with get_session() as session:
        total = session.query(SocialRecord).count()

    score = analyze({"count": total})
    return {"record_count": total, "score": score}
