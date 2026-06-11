-- Full weather dataset
SELECT * FROM weather_daily ORDER BY continent, country, city, date;

-- City-level KPI summary
SELECT city,country,continent,ROUND(AVG(avg_temp_c),2) AS avg_temperature_c,ROUND(SUM(precipitation_mm),2) AS total_precipitation_mm,ROUND(AVG(wind_speed_max_kmh),2) AS avg_wind_speed_kmh,COUNT(*) AS total_days
FROM weather_daily GROUP BY city,country,continent ORDER BY continent,country,city;

-- Continent-level weather summary
SELECT continent,ROUND(AVG(avg_temp_c),2) AS avg_temperature_c,ROUND(SUM(precipitation_mm),2) AS total_precipitation_mm,ROUND(AVG(wind_speed_max_kmh),2) AS avg_wind_speed_kmh,COUNT(DISTINCT city) AS cities
FROM weather_daily GROUP BY continent ORDER BY avg_temperature_c DESC;

-- Rainy days by city
SELECT city,country,continent,COUNT(*) AS rainy_days FROM weather_daily WHERE is_rainy_day = 1 GROUP BY city,country,continent ORDER BY rainy_days DESC;

-- Highest rainfall city
SELECT city,country,continent,ROUND(SUM(precipitation_mm),2) AS total_precipitation_mm FROM weather_daily GROUP BY city,country,continent ORDER BY total_precipitation_mm DESC LIMIT 1;
