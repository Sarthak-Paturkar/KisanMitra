import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.ui_helpers import page_header, info_box
from utils.constants import CROPS, STATES, MARKETS, MANDI_COORDINATES
from data.sample_data import generate_mock_data
from ml.preprocessor import preprocess

st.set_page_config(page_title="Weather - KisanMitra", page_icon="🌦️", layout="wide")

@st.cache_data(ttl=3600)
def fetch_weather(lat, lon):
    """Fetches 14-day historical weather from Open-Meteo."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&past_days=14&hourly=temperature_2m,precipitation&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        daily = data.get('daily', {})
        if not daily:
            return None
            
        df = pd.DataFrame({
            "Date": pd.to_datetime(daily.get('time', [])),
            "Max Temp (°C)": daily.get('temperature_2m_max', []),
            "Min Temp (°C)": daily.get('temperature_2m_min', []),
            "Rainfall (mm)": daily.get('precipitation_sum', [])
        })
        return df
    except Exception as e:
        print(f"Weather fetch error: {e}")
        return None

def weather_insights():
    page_header("🌦️", "Weather & Price Insights", "Understand weather effects on crop prices")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        crop = st.selectbox("Select Crop", CROPS, index=1)
    with col2:
        state = st.selectbox("Select State", STATES, index=0)
    with col3:
        market_list = MARKETS.get(state, ["Pune"])
        market = st.selectbox("Select Market", market_list, index=0)
        
    lat, lon = MANDI_COORDINATES.get(market, (18.5204, 73.8567)) # Default to Pune
    
    st.markdown(f"Fetching data for **{market}** (Lat: {lat:.2f}, Lon: {lon:.2f})...")
    
    weather_df = fetch_weather(lat, lon)
    if weather_df is None:
        st.error("Failed to fetch weather data. Please try again later.")
        return
        
    price_df_raw = generate_mock_data(crop, state, market, days=14)
    price_df = preprocess(price_df_raw)
    
    # Merge on Date
    weather_df['Date'] = weather_df['Date'].dt.date
    price_df['Date'] = price_df['Date'].dt.date
    merged = pd.merge(price_df, weather_df, on='Date', how='inner')
    
    # Insights
    recent_rain = merged['Rainfall (mm)'].tail(3).sum()
    if recent_rain > 20:
        info_box(f"Heavy rainfall detected recently ({recent_rain:.1f}mm). Watch out for supply disruptions.", "warn")
    elif recent_rain < 2:
        info_box("Dry weather conditions observed. Check irrigation systems.", "info")
    
    # Dual Axis Chart
    st.markdown("### Price vs Rainfall Correlation")
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Rainfall bars (Blue)
    fig.add_trace(
        go.Bar(x=merged['Date'], y=merged['Rainfall (mm)'], name="Rainfall (mm)", marker_color="rgba(66, 135, 245, 0.6)"),
        secondary_y=True,
    )
    
    # Price line (Green)
    fig.add_trace(
        go.Scatter(x=merged['Date'], y=merged['Modal_Price'], name="Price (₹)", 
                   line=dict(shape='spline', smoothing=1.3, color='#2d6a4f', width=3)),
        secondary_y=False,
    )
    
    fig.update_layout(
        plot_bgcolor="#f5f0e8",
        paper_bgcolor="rgba(0,0,0,0)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.update_yaxes(title_text="Price (₹/Quintal)", secondary_y=False)
    fig.update_yaxes(title_text="Rainfall (mm)", secondary_y=True, showgrid=False)
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### Raw Weather Data")
    st.dataframe(weather_df.sort_values(by="Date", ascending=False), use_container_width=True, hide_index=True)

if __name__ == "__main__":
    weather_insights()
