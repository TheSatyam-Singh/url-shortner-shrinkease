# ShrinkEase - Backend

Flask API for the URL shortener service.

## Setup

```bash
cd backend
pip install -r requirements.txt
```

## Configuration

Create a `.env` file (optional):

```bash
cp .env.example .env
```

Then edit values:

```
SECRET_KEY=your-secret-key
DB_PATH=./urlshortner.db
# Optional. Leave empty to auto-detect host from request
BASE_URL=
# Use * in local dev, restrict in production
CORS_ALLOWED_ORIGINS=http://localhost:5173
FLASK_DEBUG=true
PORT=4000
```

## Run

```bash
python app.py
```

The server starts on `http://localhost:4000` by default.
On Hugging Face, `PORT` is provided by the platform.

## API Routes

### URLs
- `POST /api/shorten` — Shorten a URL
- `GET /api/urls` — List all URLs
- `DELETE /api/urls/<id>` — Delete a URL
- `GET /api/urls/<id>/stats` — Get URL stats

### Redirect
- `GET /<short_code>` — Redirect to the original URL

### Health
- `GET /api/health` — Health check
