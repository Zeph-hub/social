import json
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

from app.services.apify_client import run_actor_async
from app.services.ml import analyze_text
from app.db.models import SocialPost
from app.db.session import SessionLocal

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, payload):
    with path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)


def make_safe_filename(prefix: str, platform: str, query: str) -> str:
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    safe_query = "".join([c if c.isalnum() else "_" for c in query])[:80]
    return f"{prefix}_{platform}_{safe_query}_{timestamp}.json"


def save_raw_data(platform, query, items):
    path = RAW_DIR / make_safe_filename("raw", platform, query)
    write_json(path, items)
    return path


def flatten_payload(items):
    if not isinstance(items, list):
        items = [items]

    df = pd.json_normalize(items, sep="_")
    if "text" in df.columns:
        df["content"] = df["text"]
    elif "description" in df.columns:
        df["content"] = df["description"]
    else:
        df["content"] = df.fillna("").astype(str).agg(" ".join, axis=1)

    df["content"] = df["content"].fillna("")
    df["word_count"] = np.maximum(df["content"].astype(str).str.split().apply(len).to_numpy(dtype=int), 0)
    return df


def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    languages = []
    sentiments = []

    for text in df["content"].astype(str):
        lang, sentiment = analyze_text(text)
        languages.append(lang)
        sentiments.append(sentiment)

    df["language"] = languages
    df["sentiment"] = sentiments
    return df


def save_processed_data(platform, query, df: pd.DataFrame):
    path = PROCESSED_DIR / make_safe_filename("processed", platform, query)
    write_json(path, df.to_dict(orient="records"))
    return path


def process_payload(payload):
    content = payload.get("content", "")
    if not content:
        return None

    language, sentiment = analyze_text(content)
    return {
        "content": content,
        "language": language,
        "sentiment": sentiment,
    }


async def run_pipeline(platform, query):
    data = await run_actor_async(platform, query)
    raw_path = save_raw_data(platform, query, data)
    df = flatten_payload(data)
    df = process_dataframe(df)
    processed_path = save_processed_data(platform, query, df)

    db = SessionLocal()
    try:
        for _, row in df.iterrows():
            post = SocialPost(
                platform=platform,
                content=row["content"],
                sentiment=row["sentiment"],
                language=row["language"],
            )
            db.add(post)
        db.commit()
    finally:
        db.close()

    return {
        "raw_path": str(raw_path),
        "processed_path": str(processed_path),
        "records": len(df),
    }

