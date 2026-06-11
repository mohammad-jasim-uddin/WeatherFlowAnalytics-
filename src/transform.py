from datetime import datetime, timezone
import pandas as pd

def transform_weather_data(raw_data: dict, city_config: dict) -> pd.DataFrame:
    daily = raw_data.get("daily", {})
    required = ["time","temperature_2m_max","temperature_2m_min","precipitation_sum","wind_speed_10m_max"]
    missing = [x for x in required if x not in daily]
    if missing:
        raise ValueError(f"Missing fields in API response: {missing}")
    df = pd.DataFrame({
        "date": daily["time"],
        "temperature_max_c": daily["temperature_2m_max"],
        "temperature_min_c": daily["temperature_2m_min"],
        "precipitation_mm": daily["precipitation_sum"],
        "wind_speed_max_kmh": daily["wind_speed_10m_max"],
    })
    for k in ["city","country","continent","latitude","longitude","timezone"]:
        df[k] = city_config[k]
    df["date"] = pd.to_datetime(df["date"]).dt.date.astype(str)
    for c in ["temperature_max_c","temperature_min_c","precipitation_mm","wind_speed_max_kmh"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["avg_temp_c"] = (df["temperature_max_c"] + df["temperature_min_c"]) / 2
    df["temperature_range_c"] = df["temperature_max_c"] - df["temperature_min_c"]
    df["is_rainy_day"] = df["precipitation_mm"].fillna(0).gt(0).astype(int)
    df["loaded_at_utc"] = datetime.now(timezone.utc).isoformat()
    return df[["date","city","country","continent","latitude","longitude","timezone","temperature_max_c","temperature_min_c","avg_temp_c","temperature_range_c","precipitation_mm","wind_speed_max_kmh","is_rainy_day","loaded_at_utc"]]
