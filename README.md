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


📘 User Guide — How to Use WeatherPulse

This guide explains how to run and use WeatherPulse step by step, even if you are not a developer.

1️⃣ What is WeatherPulse?

WeatherPulse is a web application that lets you:

Check current weather by city

View forecast insights (best time to go outside, rain probability, min/max temperature)

Save favorite cities

Use a simple web interface or access the API directly

2️⃣ Requirements

Before starting, make sure you have:

Python 3.11+

Node.js 18+

An OpenWeather API key (free)

3️⃣ Getting an OpenWeather API key

Go to: https://openweathermap.org/

Create a free account

Open My API Keys

Copy your API key

4️⃣ Running the Backend (API)
Step 1: Open terminal and go to backend
cd backend

Step 2: Activate virtual environment

Windows (PowerShell):

.\.venv\Scripts\Activate.ps1

Step 3: Create environment file

Create a file called .env inside backend/:

OPENWEATHER_API_KEY=YOUR_API_KEY_HERE
OPENWEATHER_BASE_URL=https://api.openweathermap.org
DEFAULT_UNITS=metric

Step 4: Start the backend server
python -m uvicorn app.main:app --reload


When successful, you will see:

Uvicorn running on http://127.0.0.1:8000

5️⃣ Using the API (Swagger UI)

Open your browser and go to:

http://127.0.0.1:8000/docs


From here you can:

Test endpoints

Send requests

See responses in real time

Available endpoints:

GET /api/weather/current

GET /api/weather/forecast

GET /api/weather/insights

POST /api/favorites

GET /api/favorites

6️⃣ Running the Frontend (Web App)
Step 1: Open a new terminal
cd frontend

Step 2: Start the frontend
npm run dev


You will see a URL like:

http://localhost:5173


Open it in your browser.

7️⃣ Using the Web Interface

Enter a city name (example: Tbilisi)

Click Load

View:

Current weather

Forecast insights

Cached status (for performance)

The frontend automatically communicates with the backend API.

8️⃣ Understanding Forecast Insights

The Insights section provides:

Min/Max temperature (next 24 hours)

Next rain time (based on probability)

Best outdoor time slot (low rain + low wind)

These insights are calculated using forecast data, not just displayed raw.

9️⃣ Running Tests (Optional)

To verify everything works correctly:

cd backend
python -m pytest


All tests should pass.

1️⃣0️⃣ Stopping the Application

Press CTRL + C in the terminal to stop backend or frontend

Close browser tabs

💡 Tips

The first API call is slower; next calls are faster due to caching

Favorites are stored locally using SQLite

The project is ready for cloud deployment
