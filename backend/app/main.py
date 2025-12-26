from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes_weather import router as weather_router
from app.api.routes_favorites import router as favorites_router
from app.core.db import engine, Base
from app.models.favorite import Favorite

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown (if needed later)
    pass

app = FastAPI(title="WeatherPulse API", version="0.1.0", lifespan=lifespan)

@app.get("/")
def root():
    return {
        "message": "WeatherPulse API is running",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(favorites_router)
app.include_router(weather_router)