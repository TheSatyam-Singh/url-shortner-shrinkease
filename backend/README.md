# ShrinkEase — Backend (Flask)

Lightweight Flask API that stores short links in a local SQLite database.

## Quick start (local)

Requirements:
- Python 3.10+
- pip

Install:

```bash
cd backend
python -m venv .venv     # optional but recommended
source .venv/bin/activate
pip install -r requirements.txt
```

Create local env file (copy example):

```bash
cp .env.example .env
# edit .env if you want to change SECRET_KEY, DB_PATH, BASE_URL, etc.
```

Run:

```bash
python app.py
```

The API listens on `http://localhost:4000` by default. Use `PORT` env var to override.

## Environment variables
- `SECRET_KEY` — Flask secret key (default in `.env.example`).
- `DB_PATH` — path to the SQLite file (default: `./urlshortner.db`).
- `BASE_URL` — optional; force the public base URL used when returning short URLs.
- `CORS_ALLOWED_ORIGINS` — comma-separated origins or `*`. You can provide origins with or without scheme — e.g. `https://app.vercel.app` **or** `app.vercel.app`. Example for a Vercel frontend:

  `CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app`

  or

  `CORS_ALLOWED_ORIGINS=your-frontend.vercel.app`

  (the server will normalize hosts without a scheme).
- `FLASK_DEBUG` — `true`/`false`.
- `PORT` — port number (Render/hosting platforms provide this).

## API endpoints
- POST `/api/shorten` — body: `{ "url": "https://...", "custom_code": "opt" }`
- GET `/api/urls` — list all short URLs
- DELETE `/api/urls/<id>` — delete a URL
- GET `/<short_code>` — redirect to original URL (302)
- GET `/api/health` — health check

## Deploy (Render)
1. Point Render to the `backend/` folder in your repo.
2. Render will run `pip install -r requirements.txt` and start `python app.py`.
3. Set environment variables on Render dashboard (SECRET_KEY, CORS_ALLOWED_ORIGINS, BASE_URL if needed).

## Notes
- `urlshortner.db` is a local SQLite DB file (safe to remove from repo). The app will create the DB schema on first run.
- For production use a managed database or persistent storage.
