from app.db.session import engine
from app.db.models import Base


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")


if __name__ == "__main__":
    init_db()
