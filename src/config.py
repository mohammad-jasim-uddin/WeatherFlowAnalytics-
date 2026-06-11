import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    database_path: str = os.getenv("DATABASE_PATH", "data/weather.db")
    forecast_days: int = int(os.getenv("FORECAST_DAYS", "7"))
