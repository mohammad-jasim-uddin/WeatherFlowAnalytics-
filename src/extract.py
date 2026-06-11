import requests
from src.config import Settings

def fetch_weather_data(city_config: dict, settings: Settings) -> dict:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": city_config["latitude"],
        "longitude": city_config["longitude"],
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max",
        "timezone": city_config["timezone"],
        "forecast_days": settings.forecast_days,
    }
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()
