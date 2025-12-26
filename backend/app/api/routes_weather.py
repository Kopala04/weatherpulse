from fastapi import APIRouter, HTTPException, Query
from httpx import HTTPStatusError

from app.services.weather_client import WeatherClient
from app.core.cache import cache_get, cache_set
from app.core.config import settings




router = APIRouter(prefix="/api/weather", tags=["weather"])
client = WeatherClient()

@router.get("/current")
async def current(city: str = Query(..., min_length=2), units: str | None = None):
    units = units or settings.default_units
    cache_key = f"weather:current:{city.lower()}:{units}"

    cached = cache_get(cache_key)
    if cached:
        # don't mutate cached object
        return {**cached, "_cached": True}

    try:
        data = await client.get_current_by_city(city=city, units=units)

        result = {
            "city": data.get("name"),
            "country": data.get("sys", {}).get("country"),
            "temp": data.get("main", {}).get("temp"),
            "feels_like": data.get("main", {}).get("feels_like"),
            "humidity": data.get("main", {}).get("humidity"),
            "wind_speed": data.get("wind", {}).get("speed"),
            "description": (data.get("weather") or [{}])[0].get("description"),
            "raw": data,
            "_cached": False,
        }

        cache_set(cache_key, result)
        return result

    except HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


@router.get("/forecast")
async def forecast(city: str = Query(..., min_length=2), units: str | None = None):
    units = units or settings.default_units
    cache_key = f"weather:forecast:{city.lower()}:{units}"

    cached = cache_get(cache_key)
    if cached:
        return {**cached, "_cached": True}

    data = await client.get_5day_3hour_by_city(city=city, units=units)
    items = []
    for it in data.get("list", []):
        items.append({
            "dt": it.get("dt"),
            "dt_txt": it.get("dt_txt"),
            "temp": it.get("main", {}).get("temp"),
            "feels_like": it.get("main", {}).get("feels_like"),
            "humidity": it.get("main", {}).get("humidity"),
            "pop": it.get("pop"),
            "wind_speed": it.get("wind", {}).get("speed"),
            "description": (it.get("weather") or [{}])[0].get("description"),
        })

    result = {
        "city": data.get("city", {}).get("name"),
        "country": data.get("city", {}).get("country"),
        "items": items,
        "_cached": False,
    }
    cache_set(cache_key, result)
    return result

@router.get("/insights")
async def insights(
    city: str = Query(..., min_length=2),
    units: str | None = None,
    rain_threshold: float = Query(0.4, ge=0.0, le=1.0),
):
    """
    Simple forecast insights based on OpenWeather 5-day/3h forecast:
    - next_rain_window: first slot where POP >= rain_threshold
    - min/max temp over next 24h
    - best_outdoor_slot: slot with lowest (POP, wind) where POP < threshold
    """
    units = units or settings.default_units
    cache_key = f"weather:insights:{city.lower()}:{units}:{rain_threshold}"

    cached = cache_get(cache_key)
    if cached:
        return {**cached, "_cached": True}

    try:
        data = await client.get_5day_3hour_by_city(city=city, units=units)
        forecast_list = data.get("list", [])

        # next ~24h => 8 slots of 3h
        window = forecast_list[:8]

        if not window:
            result = {
                "city": data.get("city", {}).get("name"),
                "country": data.get("city", {}).get("country"),
                "message": "No forecast data available",
                "_cached": False,
            }
            cache_set(cache_key, result)
            return result

        # min/max temp next 24h
        temps = [it.get("main", {}).get("temp") for it in window if it.get("main", {}).get("temp") is not None]
        min_temp_24h = min(temps) if temps else None
        max_temp_24h = max(temps) if temps else None

        # next rain slot (first POP >= threshold)
        next_rain = None
        for it in window:
            pop = it.get("pop", 0.0) or 0.0
            if pop >= rain_threshold:
                next_rain = {
                    "dt_txt": it.get("dt_txt"),
                    "pop": pop,
                    "description": (it.get("weather") or [{}])[0].get("description"),
                }
                break

        # best outdoor slot: POP < threshold, then lowest POP, then lowest wind
        candidates = []
        for it in window:
            pop = it.get("pop", 0.0) or 0.0
            wind = it.get("wind", {}).get("speed", 0.0) or 0.0
            if pop < rain_threshold:
                candidates.append((pop, wind, it))

        best_slot = None
        if candidates:
            candidates.sort(key=lambda x: (x[0], x[1]))
            _, _, it = candidates[0]
            best_slot = {
                "dt_txt": it.get("dt_txt"),
                "temp": it.get("main", {}).get("temp"),
                "wind_speed": it.get("wind", {}).get("speed"),
                "pop": it.get("pop", 0.0) or 0.0,
                "description": (it.get("weather") or [{}])[0].get("description"),
            }

        result = {
            "city": data.get("city", {}).get("name"),
            "country": data.get("city", {}).get("country"),
            "rain_threshold": rain_threshold,
            "min_temp_24h": min_temp_24h,
            "max_temp_24h": max_temp_24h,
            "next_rain_slot": next_rain,
            "best_outdoor_slot": best_slot,
            "_cached": False,
        }

        cache_set(cache_key, result)
        return result

    except HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)


