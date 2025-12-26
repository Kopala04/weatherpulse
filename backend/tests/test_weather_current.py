import pytest

from app.api import routes_weather


@pytest.mark.asyncio
async def test_weather_current_mocked(client, monkeypatch):
    async def fake_get_current_by_city(city: str, units: str | None = None) -> dict:
        return {
            "name": "Tbilisi",
            "sys": {"country": "GE"},
            "main": {"temp": 10.0, "feels_like": 8.0, "humidity": 70},
            "wind": {"speed": 2.5},
            "weather": [{"description": "clear sky"}],
        }

    # patch the instance used in routes_weather.py
    monkeypatch.setattr(routes_weather.client, "get_current_by_city", fake_get_current_by_city)

    r = await client.get("/api/weather/current?city=Tbilisi")
    assert r.status_code == 200
    data = r.json()
    assert data["city"] == "Tbilisi"
    assert data["country"] == "GE"
    assert data["temp"] == 10.0
    assert data["_cached"] is False

    # call again -> should come from cache
    r2 = await client.get("/api/weather/current?city=Tbilisi")
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2["_cached"] is True
