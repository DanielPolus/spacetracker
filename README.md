# 🚀 SpaceTracker — Space Launch ETL & Analytics Dashboard

A modern **FastAPI + PostgreSQL** data engineering backend that collects, normalizes, and visualizes **upcoming space launches**.  
Includes an **automated ETL scheduler**, **launch analytics API**, and a **Chart.js-powered dashboard**.

---

## 🌌 Features

- **FastAPI backend**
  - `/public/launches`, `/etl/run/upcoming`, `/metrics/etl`, `/scheduler`
- **ETL pipeline**
  - Periodically fetches launch data from **Launch Library API**
  - Normalizes and stores agencies, rockets, and launch info
  - Logs each ETL run with status and row count
- **Scheduler**
  - Background job via **APScheduler**
  - Runs every minute to sync new launches automatically
- **Database**
  - PostgreSQL + Alembic migrations
  - Dockerized setup (`docker compose up -d`)
- **Dashboard UI**
  - HTML + Jinja2 + Chart.js visualization
  - Launch table (scrollable) + agency/rocket stats
  - Scheduler status panel (🟢 Running / 🔴 Stopped)
- **Metrics**
  - Historical ETL logs
  - Data freshness and total rows per run

---

## 🧱 Tech Stack

**Backend**
- FastAPI (REST API)
- SQLAlchemy + Alembic (ORM & migrations)
- PostgreSQL (Dockerized)
- APScheduler (ETL background jobs)
- Pydantic v2
- Requests / AsyncIO

**Frontend**
- Jinja2 templates
- Chart.js visualization
- Pure CSS responsive layout

---

## ⚙️ Local Setup

### 1️⃣ Clone the repo
```bash
git clone https://github.com/DanielPolus/spacetracker
cd spacetracker
```
### 2️⃣ Create .env
```
DATABASE_URL=postgresql+psycopg2://space:space@localhost:5434/spacetracker
```

### 3️⃣ Start PostgreSQL
```
docker compose up -d
```

### 4️⃣ Run migrations
```
alembic upgrade head
```
### 5️⃣ Start the API
```
uvicorn app.main:app --reload
```

Then open the dashboard:
```
http://127.0.0.1:8000/dashboard
```

### 6️⃣ (Optional) Start ETL manually
```
python etl/jobs.py
```

### 7️⃣ (Optional) Enable auto-sync scheduler

Use the dashboard buttons or:

curl -X POST http://127.0.0.1:8000/scheduler/start

## 🛰 Example Output

Launch JSON sample:

{

  "id": "TEST-001",
  

  "name": "Demo Mission",
  
  "window_start": "2025-10-31T20:51:48.195233+00:00",
  
  "status": "planned",
  
  "rocket_id": "FALCON9",
  
  "agency_id": "NASA",
  
  "location": "Florida"

}

## 🧭 Project Structure

spacetracker/

│

├── app/

│   ├── api/                # REST API routes

│   ├── models/             # SQLAlchemy models

│   ├── core/               # DB & settings

│   ├── services/           # Scheduler service

│   └── ui/                 # Dashboard routes

│

├── etl/

│   ├── source_ll.py        # Fetch data from Launch Library API

│   ├── normalize.py        # Clean & standardize data

│   ├── etl_load.py         # Upsert agencies, rockets, launches

│   ├── jobs.py             # ETL job entrypoint

│   └── scheduler.py        # Background scheduler (APScheduler)

│

├── templates/              # Jinja2 templates for dashboard

├── static/                 # CSS & JS (Chart.js)

├── docker-compose.yml

└── alembic.ini
