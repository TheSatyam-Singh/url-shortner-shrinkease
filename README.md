# ShrinkEase — URL shortener

ShrinkEase is a small URL-shortening service with a React frontend and a Flask backend using SQLite. The repository contains two main components:

- `backend/` — Flask API (shorten, list, delete, redirect)
- `frontend/` — React SPA (shorten UI + list)

Live backend: https://url-shortner-shrinkease.onrender.com

## Quick start (developer)

Prerequisites:
- Python 3.10+ (for backend)
- Node.js 18+ and pnpm (for frontend)

Run backend locally:

```bash
cd backend
python -m venv .venv      # optional
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Run frontend locally:

```bash
cd frontend
pnpm install
cp .env.example .env
pnpm dev
# open http://localhost:5173
```

API example (create short URL):

```bash
curl -X POST "https://url-shortner-shrinkease.onrender.com/api/shorten" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

## Deployment notes
- Backend: deploy `backend/` to Render, Heroku, or any WSGI host. Set `SECRET_KEY` and `CORS_ALLOWED_ORIGINS` in env.
- Frontend: build with `pnpm build` and deploy static site to Netlify/Vercel/Render.

## Contribution
Open an issue or PR with changes. Keep secrets out of the repo (use `.env` and `.env.example`).

---
