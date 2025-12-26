import pytest

from app.api import routes_weather


@pytest.mark.asyncio
async def test_weather_insights_mocked(client, monkeypatch):
    async def fake_get_5day_3hour_by_city(city: str, units: str | None = None) -> dict:
        # 8 slots = ~24h
        return {
            "city": {"name": "Tbilisi", "country": "GE"},
            "list": [
                {
                    "dt_txt": "2025-01-01 00:00:00",
                    "main": {"temp": 5.0, "feels_like": 4.0, "humidity": 80},
                    "pop": 0.1,
                    "wind": {"speed": 3.0},
                    "weather": [{"description": "cloudy"}],
                },
                {
                    "dt_txt": "2025-01-01 03:00:00",
                    "main": {"temp": 4.0, "feels_like": 3.0, "humidity": 85},
                    "pop": 0.7,  # rain threshold hit here
                    "wind": {"speed": 2.0},
                    "weather": [{"description": "rain"}],
                },
            ] * 4  # make 8 items total
        }

    monkeypatch.setattr(routes_weather.client, "get_5day_3hour_by_city", fake_get_5day_3hour_by_city)

    r = await client.get("/api/weather/insights?city=Tbilisi&rain_threshold=0.6")
    assert r.status_code == 200
    data = r.json()

    assert data["city"] == "Tbilisi"
    assert data["country"] == "GE"
    assert data["min_temp_24h"] is not None
    assert data["max_temp_24h"] is not None
    assert data["next_rain_slot"] is not None
    assert data["next_rain_slot"]["pop"] >= 0.6
    assert data["_cached"] is False

    # second call -> cached
    r2 = await client.get("/api/weather/insights?city=Tbilisi&rain_threshold=0.6")
    assert r2.status_code == 200
    assert r2.json()["_cached"] is True
