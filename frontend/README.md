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

Configure the backend API URL:

```
VITE_API_BASE_URL=https://url-shortner-shrinkease.onrender.com
```

For local development, you can set it to:

```
VITE_API_BASE_URL=http://localhost:4000
```

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