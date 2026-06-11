import sqlite3
import pandas as pd

def read_sql(database_path: str, query: str, params=()):
    with sqlite3.connect(database_path) as con:
        return pd.read_sql_query(query, con, params=params)

def get_weather_data(database_path: str) -> pd.DataFrame:
    return read_sql(database_path, "SELECT * FROM weather_daily ORDER BY continent,country,city,date")

def get_summary_metrics(database_path: str, city: str) -> dict:
    q = """SELECT city,country,continent,ROUND(AVG(avg_temp_c),2) avg_temp_c,ROUND(SUM(precipitation_mm),2) total_precipitation_mm,ROUND(AVG(wind_speed_max_kmh),2) avg_wind_speed_kmh,COUNT(*) forecast_days FROM weather_daily WHERE city=? GROUP BY city,country,continent"""
    r = read_sql(database_path, q, (city,))
    return r.iloc[0].to_dict() if not r.empty else {"city":city,"avg_temp_c":0,"total_precipitation_mm":0,"avg_wind_speed_kmh":0,"forecast_days":0}

def get_country_summary(database_path: str) -> pd.DataFrame:
    return read_sql(database_path, """SELECT country,continent,ROUND(AVG(avg_temp_c),2) avg_temp_c,ROUND(SUM(precipitation_mm),2) total_precipitation_mm,ROUND(AVG(wind_speed_max_kmh),2) avg_wind_speed_kmh,COUNT(DISTINCT city) cities FROM weather_daily GROUP BY country,continent ORDER BY continent,country""")

def get_continent_summary(database_path: str) -> pd.DataFrame:
    return read_sql(database_path, """SELECT continent,ROUND(AVG(avg_temp_c),2) avg_temp_c,ROUND(SUM(precipitation_mm),2) total_precipitation_mm,ROUND(AVG(wind_speed_max_kmh),2) avg_wind_speed_kmh,COUNT(DISTINCT city) cities FROM weather_daily GROUP BY continent ORDER BY avg_temp_c DESC""")

def get_rainy_days(database_path: str, city: str) -> int:
    r = read_sql(database_path, "SELECT COUNT(*) rainy_days FROM weather_daily WHERE city=? AND is_rainy_day=1", (city,))
    return int(r.iloc[0]["rainy_days"])

def get_temperature_extremes(database_path: str, city: str) -> pd.DataFrame:
    hot = read_sql(database_path, "SELECT 'Hottest Day' metric,date,city,country,continent,temperature_max_c value_c FROM weather_daily WHERE city=? ORDER BY temperature_max_c DESC LIMIT 1", (city,))
    cold = read_sql(database_path, "SELECT 'Coldest Day' metric,date,city,country,continent,temperature_min_c value_c FROM weather_daily WHERE city=? ORDER BY temperature_min_c ASC LIMIT 1", (city,))
    return pd.concat([hot,cold], ignore_index=True)
