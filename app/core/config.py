import os
from dotenv import load_dotenv

load_dotenv()

class settings:
    Apify_token: str = os.getenv("APIFY_TOKEN")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    APIFY_BASE_URL: str = os.getenv("APIFY_BASE_URL", "https://api.apify.com")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
settings = settings()