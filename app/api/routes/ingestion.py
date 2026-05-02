from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.pipeline import process_payload


class IngestionItem(BaseModel):
    content: str


router = APIRouter()


@router.post("/")
async def ingest(item: IngestionItem):
    result = process_payload(item.dict())
    if not result:
        raise HTTPException(status_code=400, detail="Invalid payload")
    return {"status": "ok", "processed": result}
