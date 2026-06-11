from src.config import Settings
from src.cities import CITIES
from src.extract import fetch_weather_data
from src.transform import transform_weather_data
from src.load import load_weather_data

def main() -> None:
    settings = Settings()
    frames = []
    print("Starting WeatherFlow multi-city ETL pipeline...")
    for city in CITIES:
        print(f"Extracting {city['city']}, {city['country']} ({city['continent']})")
        raw = fetch_weather_data(city, settings)
        frames.append(transform_weather_data(raw, city))
    load_weather_data(frames, settings.database_path)
    print(f"ETL completed. Cities: {len(frames)} | Rows: {sum(len(f) for f in frames)} | DB: {settings.database_path}")

if __name__ == "__main__":
    main()
