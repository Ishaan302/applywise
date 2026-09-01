# Applywise

A full-stack web app to log, manage, and analyse job applications — built to replace the messy spreadsheet most students use to track internship and job hunts.

## Why

When you're applying to dozens of companies, spreadsheets fall apart fast. There's no reminder system, no visual progress, and no way to tell your response rate or which platforms actually work. This app replaces that spreadsheet with structured data, a clean dashboard, and real analytics.

## Features

- **Application tracking** — log company, role, location, salary, source, resume version, and notes for every application
- **Status pipeline** — move applications through Saved → Applied → OA → Interview → Offer → Rejected → Withdrawn
- **Interview rounds** — log each round separately (phone screen, technical, HR, system design) with outcome and notes
- **Dashboard** — total applications, response rate, interview conversion rate, offer rate, applications per week
- **Analytics** — weekly volume trends, status funnel, company response comparison, application heatmap, salary distribution
- **Resume matcher** — paste a job description and compare it against your resume to get a match score and a list of missing keywords
- **Search, filter, and sort** — by company, role, status, source, date range, or salary range
- **CSV export** — export all applications or a filtered subset
- **Accounts** — register and log in, with all data scoped to your own account

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
| Charts | Recharts |
| HTTP client | Axios |
| Containers | Docker + docker-compose |

## Project Structure

```
applywise/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── routers/
│   │   │   ├── applications.py
│   │   │   ├── auth.py
│   │   │   └── analytics.py
│   │   └── utils/
│   │       ├── auth.py
│   │       └── analytics_engine.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   └── api/
│   └── package.json
└── docker-compose.yml
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js
- Docker (recommended, for Postgres and full setup)

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

## What This Project Doesn't Do

- No auto-apply or scraping of job platforms
- No email integration (no reading Gmail/Outlook to detect replies)
- No push notifications — web only
- No multi-user teams or shared dashboards
- No resume file storage — resume versions are tagged by name only
- No calendar integration
- No mobile app — the web app is responsive but there's no native app

## License

MIT
