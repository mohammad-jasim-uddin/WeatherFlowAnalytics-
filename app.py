from pathlib import Path
import plotly.express as px
import streamlit as st
from src.config import Settings
from src.analytics import get_weather_data, get_summary_metrics, get_country_summary, get_continent_summary, get_rainy_days, get_temperature_extremes

st.set_page_config(page_title="WeatherFlow Analytics", page_icon="🌦️", layout="wide")
settings = Settings()
db_path = Path(settings.database_path)
st.title("🌦️ WeatherFlow Analytics")
st.caption("Multi-City ETL Pipeline: Python → SQL → SQLite → Streamlit Dashboard")
if not db_path.exists():
    st.error("Database not found. Run `python run_etl.py` first."); st.stop()
df = get_weather_data(settings.database_path)
if df.empty:
    st.warning("No weather data found. Run `python run_etl.py`."); st.stop()
st.sidebar.header("Filters")
continents = ["All"] + sorted(df["continent"].unique())
selected_continent = st.sidebar.selectbox("Select Continent", continents)
filtered_df = df if selected_continent == "All" else df[df["continent"] == selected_continent]
countries = ["All"] + sorted(filtered_df["country"].unique())
selected_country = st.sidebar.selectbox("Select Country", countries)
if selected_country != "All": filtered_df = filtered_df[filtered_df["country"] == selected_country]
selected_city = st.sidebar.selectbox("Select City", sorted(filtered_df["city"].unique()))
city_df = filtered_df[filtered_df["city"] == selected_city].copy()
summary = get_summary_metrics(settings.database_path, selected_city)
rainy_days = get_rainy_days(settings.database_path, selected_city)
extremes = get_temperature_extremes(settings.database_path, selected_city)
col1,col2,col3,col4 = st.columns(4)
col1.metric("Average Temp °C", f"{summary['avg_temp_c']:.1f}")
col2.metric("Total Rain mm", f"{summary['total_precipitation_mm']:.1f}")
col3.metric("Average Wind km/h", f"{summary['avg_wind_speed_kmh']:.1f}")
col4.metric("Rainy Days", int(rainy_days))
st.markdown("---")
st.subheader("Global City Comparison")
comparison_col1, comparison_col2 = st.columns(2)
with comparison_col1:
    city_summary = filtered_df.groupby(["continent","country","city"], as_index=False).agg(avg_temp_c=("avg_temp_c","mean"), total_precipitation_mm=("precipitation_mm","sum"), avg_wind_speed_kmh=("wind_speed_max_kmh","mean")).round(2)
    fig = px.bar(city_summary, x="city", y="avg_temp_c", color="continent", title="Average Temperature by City", labels={"avg_temp_c":"Average Temperature °C"})
    st.plotly_chart(fig, use_container_width=True)
with comparison_col2:
    continent_summary = get_continent_summary(settings.database_path)
    fig = px.bar(continent_summary, x="continent", y="avg_temp_c", title="Average Temperature by Continent", labels={"avg_temp_c":"Average Temperature °C"})
    st.plotly_chart(fig, use_container_width=True)
st.markdown("---")
left,right = st.columns(2)
with left:
    fig = px.line(city_df, x="date", y=["temperature_max_c","temperature_min_c","avg_temp_c"], markers=True, title=f"Temperature Trend — {selected_city}", labels={"value":"Temperature °C"})
    st.plotly_chart(fig, use_container_width=True)
with right:
    fig = px.bar(filtered_df, x="date", y="precipitation_mm", color="city", title="Daily Precipitation by City", labels={"precipitation_mm":"Precipitation mm"})
    st.plotly_chart(fig, use_container_width=True)
fig = px.line(city_df, x="date", y="wind_speed_max_kmh", markers=True, title=f"Maximum Daily Wind Speed — {selected_city}", labels={"wind_speed_max_kmh":"Wind Speed km/h"})
st.plotly_chart(fig, use_container_width=True)
st.markdown("---")
left,right = st.columns(2)
with left:
    st.subheader("Temperature Extremes")
    st.dataframe(extremes, use_container_width=True)
with right:
    st.subheader("Country-Level SQL Summary")
    st.dataframe(get_country_summary(settings.database_path), use_container_width=True)
with st.expander("View Raw Weather Data"):
    st.dataframe(filtered_df, use_container_width=True)
