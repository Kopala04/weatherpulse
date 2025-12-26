# WeatherPulse 🌦️
A FastAPI-based weather forecasting platform with caching, favorites persistence, forecast insights, automated tests, and CI.

## Features
- **Current weather** by city (`/api/weather/current`)
- **5-day / 3-hour forecast** (`/api/weather/forecast`)
- **Forecast insights** (`/api/weather/insights`)  
  - next rain slot, min/max temp (next 24h), best outdoor slot
- **Caching layer** (in-memory TTL cache; Redis-ready)
- **Favorites persistence** (SQLAlchemy + SQLite)
- **Automated tests** (pytest + pytest-asyncio) with **mocked external API calls**
- **CI** via GitHub Actions (`.github/workflows/tests.yml`)

## Tech Stack
- Backend: **Python**, **FastAPI**, **httpx**
- Persistence: **SQLAlchemy** (SQLite for local dev; Postgres-ready)
- Testing: **pytest**, **pytest-asyncio**
- CI: **GitHub Actions**
- Frontend (optional): **React + Vite** (charts, search, favorites)

---

## API Docs
Run the backend and open:
- Swagger UI: `http://127.0.0.1:8000/docs`

---

## Local Setup (Backend)
### 1) Create venv and install dependencies
```bash
cd backend
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -r requirements.txt
