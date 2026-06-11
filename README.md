# WeatherFlow Analytics — Multi-City End-to-End ETL & Dashboard Project

A complete Python → SQL → Dashboard project using Open-Meteo weather data for 10 global cities across Europe, Asia, Africa, North America, South America, and Oceania.

## Cities Included

London, Paris, New York, Toronto, Dhaka, Dubai, Tokyo, Sydney, Cape Town, and Sao Paulo.

## Skills Demonstrated

Python, Pandas, REST API integration, ETL, SQL, SQLite, Streamlit, Plotly, dashboarding, country-level analytics, continent-level analytics, analytics storytelling.

## Architecture

```text
Open-Meteo API → Python Extract → Pandas Transform → SQLite Load → SQL Queries → Streamlit Dashboard
```

## Run Locally

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate # Mac/Linux
pip install -r requirements.txt
python run_etl.py
streamlit run app.py
```

## Dashboard Features

- Continent, country, and city filters
- KPI cards
- City temperature comparison
- Continent temperature comparison
- Rainfall comparison
- Wind speed trend
- SQL summary tables
- Raw data explorer


**WeatherFlow Analytics — Multi-City End-to-End ETL & Dashboard Project**  
Built a full ETL pipeline using Python, Pandas, SQL, SQLite, and Streamlit. Extracted multi-city weather data from Open-Meteo API across Europe, Asia, Africa, North America, South America, and Oceania. Cleaned and transformed JSON data, stored city, country, and continent-level records in a relational database, wrote SQL queries for KPIs, and created an interactive dashboard to compare temperature, rainfall, and wind-speed trends across global cities.
# WeatherFlowAnalytics-
