import httpx
from app.core.config import settings


class WeatherClient:
    def __init__(self) -> None:
        self.base_url = settings.openweather_base_url
        self.api_key = settings.openweather_api_key

    async def get_current_by_city(self, city: str, units: str | None = None) -> dict:
        units = units or settings.default_units
        url = f"{self.base_url}/data/2.5/weather"
        params = {"q": city, "appid": self.api_key, "units": units}

        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url, params=params)
            r.raise_for_status()
            return r.json()

    async def get_5day_3hour_by_city(self, city: str, units: str | None = None) -> dict:
        units = units or settings.default_units
        url = f"{self.base_url}/data/2.5/forecast"
        params = {"q": city, "appid": self.api_key, "units": units}

        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url, params=params)
            r.raise_for_status()
            return r.json()
