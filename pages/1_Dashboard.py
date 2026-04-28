import streamlit as st
import pandas as pd
import sys
import os

# Ensure imports work when run as a page
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.ui_helpers import page_header, metric_card
from utils.constants import CROPS, STATES, MARKETS
from utils.charts import make_price_chart
from data.sample_data import generate_mock_data
from ml.preprocessor import preprocess

st.set_page_config(page_title="Dashboard - KisanMitra", page_icon="🌱", layout="wide")

def load_data(crop, state, market):
    # In a real app, this would fetch from DB. We use sample data here.
    raw_df = generate_mock_data(crop, state, market, days=365)
    clean_df = preprocess(raw_df)
    return raw_df, clean_df

def dashboard():
    page_header("🌱", "Market Dashboard", "Live crop price overview")
    
    # Selectors
    col1, col2, col3 = st.columns(3)
    with col1:
        crop = st.selectbox("Select Crop", CROPS, index=0)
    with col2:
        state = st.selectbox("Select State", STATES, index=0)
    with col3:
        market_list = MARKETS.get(state, ["Unknown"])
        market = st.selectbox("Select Market", market_list, index=0)
        
    # Load Data
    raw_df, df = load_data(crop, state, market)
    
    # Calculate metrics
    latest_price = df['Modal_Price'].iloc[-1]
    prev_price = df['Modal_Price'].iloc[-2]
    pct_change = ((latest_price - prev_price) / prev_price) * 100
    
    # Mock some extra metrics for the dashboard
    top_gainer = "Onion (+5.2%)" if crop != "Onion" else "Tomato (+4.1%)"
    biggest_drop = "Potato (-2.3%)" if crop != "Potato" else "Wheat (-1.5%)"
    
    # Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        delta_str = f"{pct_change:.1f}%" if pct_change >= 0 else f"{pct_change:.1f}%"
        metric_card(f"{crop} Price", f"₹{latest_price:.0f}", delta_str, "💰")
    with m2:
        metric_card("Top Gainer", top_gainer, "", "📈")
    with m3:
        metric_card("Biggest Drop", biggest_drop, "", "📉")
    with m4:
        metric_card("Active Markets", "34", "+2 this week", "🏪")
        
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Price History", "📅 30-Day Forecast", "❄️ Seasonality"])
    
    with tab1:
        st.markdown(f"### {crop} Price History (Past Year)")
        fig = make_price_chart(df['Date'], df['Modal_Price'], crop_name=crop)
        st.plotly_chart(fig, use_container_width=True)
        
    with tab2:
        st.info("Head over to the **Predict** page for detailed forecasting using our Ensemble AI models!")
        
    with tab3:
        # Simple monthly average for seasonality
        df['Month'] = df['Date'].dt.month
        monthly_avg = df.groupby('Month')['Modal_Price'].mean().reset_index()
        import plotly.express as px
        fig = px.bar(monthly_avg, x='Month', y='Modal_Price', title="Average Price by Month",
                     color_discrete_sequence=['#2d6a4f'])
        st.plotly_chart(fig, use_container_width=True)

    # Raw Data
    with st.expander("View Raw Data"):
        st.dataframe(df.tail(30).sort_values(by="Date", ascending=False), use_container_width=True)

if __name__ == "__main__":
    dashboard()
