import logging

import httpx
from app.core.config import settings

BASE_URL = settings.APIFY_BASE_URL.rstrip("/")
logger = logging.getLogger(__name__)

ACTOR_IDS = {
    "tiktok": settings.APIFY_TIKTOK_ACTOR_ID,
}


async def run_actor_async(platform: str, query: str) -> list:
    actor_id = ACTOR_IDS.get(platform.lower())
    if not actor_id:
        logger.warning("Unsupported platform: %s", platform)
        return []

    if not settings.APIFY_TOKEN:
        logger.warning("Missing APIFY_TOKEN for Apify requests")
        return []

    url = f"{BASE_URL}/v2/acts/{actor_id}/runs"
    params = {"token": settings.APIFY_TOKEN, "waitForFinish": 1}
    payload = {"input": {"query": query}}

    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(url, params=params, json=payload)
        response.raise_for_status()
        run_data = response.json()

        dataset_id = run_data.get("defaultDatasetId")
        if dataset_id:
            dataset_url = f"{BASE_URL}/v2/datasets/{dataset_id}/items"
            dataset_resp = await client.get(dataset_url, params={"token": settings.APIFY_TOKEN})
            dataset_resp.raise_for_status()
            return dataset_resp.json()

        return run_data.get("output", [])
