# Social Analytics Platform

A lightweight social analytics service that ingests TikTok hashtag data via Apify, stores posts in PostgreSQL, and exposes a simple sentiment summary endpoint.

## Features

- Ingest social content via a background task
- Extract sentiment and language from text
- Store post data in PostgreSQL
- Expose a summary endpoint for sentiment counts
- Support Apify TikTok actor integration

## Requirements

- Python 3.12+
- Docker and Docker Compose
- PostgreSQL (via Docker Compose or external service)

## Setup

1. Install Python dependencies:

```bash
cd /workspaces/social
pip install -r requirements.txt
```

2. Copy `.env` and set your environment values:

```bash
cp .env.example .env
```

3. Update `.env` with production-ready values:

- `DATABASE_URL`: e.g. `postgresql://social:social@localhost:5432/social`
- `APIFY_BASE_URL`: `https://api.apify.com`
- `APIFY_TOKEN`: your Apify API token
- `APIFY_TIKTOK_ACTOR_ID`: `coregent~tiktok-hashtag-scraper`

> Do not commit secrets like `APIFY_TOKEN` to source control.

## Local database initialization

If you are using the provided Docker Compose PostgreSQL service:

```bash
docker compose up -d db
```

Then initialize the schema:

```bash
PYTHONPATH=. python scripts/init_db.py
```

## Running the app

### Python development mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Docker Compose deployment

```bash
docker compose up -d --build web worker
```

This will start:

- `web` service on port `8000`
- `worker` service to process ingestion jobs
- `db` service if included and running

## API Endpoints

- `POST /ingest?platform=tiktok&query=<hashtag>`
  - Starts background ingestion for the specified platform and query
- `GET /sentiment_summary`
  - Returns sentiment counts for stored posts

## Notes

- The project currently uses a default Hugging Face sentiment pipeline. In production, pin the model explicitly and configure an HF token if needed.
- Ensure `APIFY_TIKTOK_ACTOR_ID` is set to `coregent~tiktok-hashtag-scraper` for the TikTok hashtag scraper actor.
- If you need to initialize the database manually with SQLite, set `DATABASE_URL=sqlite:///./social.db` in `.env`.

