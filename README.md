# Applywise

![CI](https://github.com/Ishaan302/applywise/actions/workflows/ci.yml/badge.svg)

A full-stack web app to log, manage, and analyse job applications — built to replace the messy spreadsheet most students use to track internship and job hunts.

## Why

When you're applying to dozens of companies, spreadsheets fall apart fast. There's no reminder system, no visual progress, and no way to tell your response rate or which platforms actually work. This app replaces that spreadsheet with structured data, a clean dashboard, and real analytics.

## Features

- **Application tracking** — log company, role, location, source, job URL, salary, resume version, and notes for every application
- **Status pipeline** — move applications through Saved → Applied → OA → Interview → Offer → Rejected → Withdrawn
- **Interview rounds** — log each round separately (phone screen, technical, HR, system design) with outcome and notes
- **Dashboard** — total applications, response rate, interview conversion rate, offer rate
- **Analytics endpoints** — weekly application volume and status funnel (backend complete; frontend charts not yet built)
- **Accounts** — register and log in with JWT, all data scoped to your own account
- **Automated tests** — 11 pytest tests covering auth, CRUD, user isolation, and analytics, run on every push via GitHub Actions
- **One-command local setup** — full stack (Postgres + backend + frontend) via Docker Compose

## Tech Stack

| Layer | Tech |
|-------|------|
| Backend | FastAPI (Python) |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Auth | JWT + bcrypt |
| Analytics | Pandas |
| Frontend | React + Vite |
| Styling | Tailwind CSS |
| HTTP client | Axios |
| Containers | Docker + Docker Compose |
| Tests | pytest + httpx |
| CI | GitHub Actions |


## Project Structure

```
applywise/
├── backend/
│ ├── app/
│ │ ├── main.py
│ │ ├── database.py
│ │ ├── models.py
│ │ ├── schemas.py
│ │ └── utils/
│ │ ├── auth.py
│ │ └── analytics_engine.py
│ ├── tests/
│ │ ├── conftest.py
│ │ ├── test_auth.py
│ │ ├── test_applications.py
│ │ └── test_analytics.py
│ ├── Dockerfile
│ ├── requirements.txt
│ └── .env # not committed — see setup below
├── frontend/
│ ├── src/
│ │ ├── pages/ # Login, Dashboard, Applications
│ │ ├── components/ # PrivateRoute
│ │ └── api/client.js
│ ├── Dockerfile
│ └── package.json
├── .github/workflows/ci.yml
└── docker-compose.yml


```
## Getting Started

### Option A — Docker Compose (recommended)

```bash
git clone https://github.com/Ishaan302/applywise.git
cd applywise
docker compose up --build
```

- Backend API docs: `http://localhost:8000/docs`
- Frontend: `http://localhost:5173`

Postgres, the backend, and the frontend all start together, correctly wired, with hot-reload on both backend and frontend code.

### Option B — Manual setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

# start Postgres locally
docker run --name jobtracker-db \
  -e POSTGRES_USER=ishaan \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=jobtracker \
  -p 5432:5432 -d postgres

# set environment variables
cp .env.example .env   # then fill in DATABASE_URL and SECRET_KEY

uvicorn app.main:app --reload
```

API docs available at `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App available at `http://localhost:5173`.

### Or run everything with Docker

```bash
docker-compose up --build
```
## Run tests

```bash
cd backend
pytest tests/ -v
```

## API Overview

```
Auth
  POST   /auth/register
  POST   /auth/login

Applications
  GET    /applications
  POST   /applications
  GET    /applications/{id}
  PATCH  /applications/{id}
  DELETE /applications/{id}
  GET    /applications/export/csv

Interview Rounds
  GET    /applications/{id}/rounds
  POST   /applications/{id}/rounds
  PATCH  /applications/{id}/rounds/{round_id}
  DELETE /applications/{id}/rounds/{round_id}

Analytics
  GET    /analytics/stats
  GET    /analytics/funnel
  GET    /analytics/weekly
  GET    /analytics/sources

Resume Matcher
  POST   /match

User
  GET    /users/me
  PATCH  /users/me
  DELETE /users/me
```


## Roadmap

Not built yet — listed here rather than in Features above, since none of these exist in the app right now:

- Analytics page with actual charts (Recharts) — endpoints exist, frontend visualization doesn't
- Resume ↔ job description matcher (keyword overlap, then sentence-embedding similarity)
- Search, filter, and sort on the applications list
- CSV export
- Settings page (change password, delete account)
- Alembic migrations (currently using `create_all()`)
- Rate limiting on auth endpoints
- Deployed live demo

## What This Project Doesn't Do (by design)

- No auto-apply or scraping of job platforms
- No email integration (no reading Gmail/Outlook to detect replies)
- No push notifications — web only
- No multi-user teams or shared dashboards
- No resume file storage — resume versions are tagged by name only
- No calendar integration
- No mobile app — the web app is responsive but there's no native app

## License

MIT
