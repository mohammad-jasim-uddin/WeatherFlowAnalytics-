from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS weather_daily (
    date TEXT NOT NULL, city TEXT NOT NULL, country TEXT NOT NULL, continent TEXT NOT NULL,
    latitude REAL, longitude REAL, timezone TEXT, temperature_max_c REAL, temperature_min_c REAL,
    avg_temp_c REAL, temperature_range_c REAL, precipitation_mm REAL, wind_speed_max_kmh REAL,
    is_rainy_day INTEGER, loaded_at_utc TEXT, PRIMARY KEY (date, city)
);
"""

def load_weather_data(dataframes: list[pd.DataFrame], database_path: str) -> None:
    db_file = Path(database_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)
    df = pd.concat(dataframes, ignore_index=True)
    engine = create_engine(f"sqlite:///{database_path}")
    with engine.begin() as con:
        con.execute(text(CREATE_TABLE_SQL))
        for _, row in df.iterrows():
            con.execute(text("""
                INSERT OR REPLACE INTO weather_daily (date,city,country,continent,latitude,longitude,timezone,temperature_max_c,temperature_min_c,avg_temp_c,temperature_range_c,precipitation_mm,wind_speed_max_kmh,is_rainy_day,loaded_at_utc)
                VALUES (:date,:city,:country,:continent,:latitude,:longitude,:timezone,:temperature_max_c,:temperature_min_c,:avg_temp_c,:temperature_range_c,:precipitation_mm,:wind_speed_max_kmh,:is_rainy_day,:loaded_at_utc)
            """), row.to_dict())
