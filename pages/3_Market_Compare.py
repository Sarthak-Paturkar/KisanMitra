import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.ui_helpers import page_header, info_box
from utils.constants import CROPS, STATES, MARKETS
from data.sample_data import generate_mock_data
from ml.preprocessor import preprocess

st.set_page_config(
    page_title="Compare - KisanMitra",
    page_icon="🗺️",
    layout="wide"
)


def market_compare():

    page_header(
        "🗺️",
        "Market Comparison",
        "Compare prices across mandis"
    )

    # ---------------- Filters ----------------
    col1, col2 = st.columns(2)

    with col1:
        crop = st.selectbox(
            "Select Crop",
            CROPS
        )

        state = st.selectbox(
            "Select State",
            STATES
        )

    market_list = MARKETS.get(state, [])

    with col2:
        selected_markets = st.multiselect(
            "Select Markets to Compare (Up to 3)",
            market_list,
            default=market_list[:min(2, len(market_list))]
        )

    if not selected_markets:
        st.warning("Please select at least one market.")
        return

    if len(selected_markets) > 3:
        st.error("Maximum 3 markets allowed.")
        return


    # ---------------- Load Market Data ----------------
    market_data = {}
    latest_prices = {}

    for market in selected_markets:

        raw_df = generate_mock_data(
            crop,
            state,
            market,
            days=30
        )

        df = preprocess(raw_df)

        market_data[market] = df
        latest_prices[market] = df["Modal_Price"].iloc[-1]


    # ================= SUMMARY =================
    st.markdown(f"## Current Price Summary for {crop}")

    best_market = max(
        latest_prices,
        key=latest_prices.get
    )

    info_box(
        f"**Best Price:** ₹{latest_prices[best_market]:.0f} in **{best_market}**",
        "info"
    )


    summary_rows = []

    for market in selected_markets:

        today_price = round(
            latest_prices[market],
            0
        )

        avg_7 = round(
            market_data[market]["Modal_Price"].tail(7).mean(),
            0
        )

        summary_rows.append({
            "Market": market,
            "Today's Price (₹)": f"{today_price:.0f}",
            "7-Day Avg (₹)": f"{avg_7:.0f}"
        })

    summary_df = pd.DataFrame(summary_rows)


    # Uniform font + consistent summary block
    st.table(summary_df)



    # ================= PRICE TREND CHART =================
    st.markdown(
        "## Price Trend Comparison (Last 30 Days)"
    )

    fig = go.Figure()

    colors = [
        "#2d6a4f",
        "#f4a261",
        "#264653"
    ]

    for i, market in enumerate(selected_markets):

        df = market_data[market]

        fig.add_trace(
            go.Scatter(
                x=df["Date"],
                y=df["Modal_Price"],
                mode="lines",
                name=market,
                line=dict(
                    shape="spline",
                    smoothing=1.3,
                    width=3,
                    color=colors[i]
                )
            )
        )


    fig.update_layout(
        plot_bgcolor="#f5f0e8",
        paper_bgcolor="rgba(0,0,0,0)",
        hovermode="x unified",

        xaxis=dict(
            showgrid=False
        ),

        yaxis=dict(
            title="₹ / Quintal",
            showgrid=True,
            gridcolor="rgba(0,0,0,0.05)"
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),

        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


if __name__ == "__main__":
    market_compare()