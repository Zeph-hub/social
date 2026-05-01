from app.services.apify_client import run_actor_async
from app.services.ml import analyze_text
from app.db.models import SocialPost
from app.db.session import SessionLocal

async def run_pipeline(platform, query):
    data = await run_actor_async(platform, query)
    db = SessionLocal()

    for item in data:
        text = item.get("text", "")
        lang, sentiment = analyze_text(text)

        post = SocialPost(
            platform=platform,
            content=text,
            sentiment=sentiment,
            language=lang
        )
        db.add(post)
    db.commit()
    db.close()

