import logging
import time

from app.core.logging import configure_logging
from app.db.models import SocialPost
from app.db.session import get_session

configure_logging()
logger = logging.getLogger(__name__)


def run_worker(poll_interval: int = 15) -> None:
    logger.info("Worker started, polling every %s seconds", poll_interval)
    while True:
        with get_session() as session:
            total = session.query(SocialPost).count()
            logger.info("Stored %s social post(s)", total)

        time.sleep(poll_interval)


if __name__ == "__main__":
    run_worker()
