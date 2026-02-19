# ShrinkEase - Frontend

React app for the URL shortener.

## Setup

```bash
cd frontend
pnpm install
```

## Environment Configuration

Create a `.env` file in the frontend directory (or copy from `.env.example`):

```bash
cp .env.example .env
```

Configure the backend API URL locally or for production:

```
# Production (Render backend)
VITE_API_BASE_URL=https://url-shortner-shrinkease.onrender.com

# Local development
VITE_API_BASE_URL=http://localhost:4000
```

If deploying the frontend to Vercel, set the **VITE_API_BASE_URL** environment variable in the Vercel dashboard. Also ensure the backend's `CORS_ALLOWED_ORIGINS` includes your Vercel origin (for example: `your-app.vercel.app` or `https://your-app.vercel.app`).

Example steps on Vercel:
1. Project → Settings → Environment Variables → add `VITE_API_BASE_URL` = `https://url-shortner-shrinkease.onrender.com`
2. Redeploy the Vercel site.

On the backend (Render) make sure `CORS_ALLOWED_ORIGINS` includes the Vercel origin (or use `*` for quick testing).

## Development

```bash
pnpm dev
```

Runs on `http://localhost:5173` and connects to the backend URL specified in `.env`.

## Build

```bash
pnpm build
```
\



curl -X POST "https://url-shortner-shrinkease.onrender.com/api/shorten" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'