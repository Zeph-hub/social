import logging
import requests

from app.core.config import settings

logger = logging.getLogger(__name__)


def fetch_social_data(query: str) -> dict:
    try:
        response = requests.get(
            f"{settings.apify_base_url}/v2/actor-tasks",
            params={"q": query, "token": settings.apify_token},
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        logger.warning("Failed to fetch social data: %s", exc)
        return {}
