import logging
import time

from app.core.logging import configure_logging
from app.db.models import SocialRecord
from app.db.session import get_session
from app.services.ml import analyze

configure_logging()
logger = logging.getLogger(__name__)


def run_worker(poll_interval: int = 15) -> None:
    logger.info("Worker started, polling every %s seconds", poll_interval)
    while True:
        with get_session() as session:
            total = session.query(SocialRecord).count()
            score = analyze({"count": total})
            logger.info("Processed %s record(s): score=%s", total, score)

        time.sleep(poll_interval)


if __name__ == "__main__":
    run_worker()
