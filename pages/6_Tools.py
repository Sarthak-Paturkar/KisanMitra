import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.ui_helpers import page_header, info_box
from utils.constants import CROPS, STATES, MARKETS
from utils.db import save_alert, get_active_alerts

st.set_page_config(page_title="Tools - KisanMitra", page_icon="🛠️", layout="wide")

def tools_page():
    page_header("🛠️", "Farmer Tools", "Profit calculators and price alerts")
    
    tab1, tab2 = st.tabs(["💰 Profit Calculator", "🔔 Price Alerts"])
    
    with tab1:
        st.markdown("### Estimate Your Profit")
        col1, col2 = st.columns(2)
        
        with col1:
            crop = st.selectbox("Crop", CROPS, key="calc_crop")
            expected_yield = st.number_input("Expected Yield (Quintals)", min_value=1.0, value=50.0)
            target_price = st.number_input("Target Price (₹/Quintal)", min_value=100, value=1500)
            
        with col2:
            seed_cost = st.number_input("Seed Cost (₹)", min_value=0, value=5000)
            fert_cost = st.number_input("Fertilizer/Pesticide Cost (₹)", min_value=0, value=8000)
            labor_cost = st.number_input("Labor & Transport Cost (₹)", min_value=0, value=12000)
            other_cost = st.number_input("Other Costs (₹)", min_value=0, value=2000)
            
        total_cost = seed_cost + fert_cost + labor_cost + other_cost
        expected_revenue = expected_yield * target_price
        profit = expected_revenue - total_cost
        
        st.markdown("---")
        res_col1, res_col2, res_col3 = st.columns(3)
        res_col1.metric("Total Cost", f"₹{total_cost:,.2f}")
        res_col2.metric("Expected Revenue", f"₹{expected_revenue:,.2f}")
        
        profit_color = "#2d6a4f" if profit >= 0 else "#c5221f"
        res_col3.markdown(f"<div style='background-color: white; padding: 1rem; border-radius: 8px; border-left: 4px solid {profit_color}; box-shadow: 0 2px 4px rgba(0,0,0,0.05);'><div style='font-size:0.9rem; color:#666;'>Net Profit / Loss</div><div style='font-size: 1.8rem; font-weight: bold; color: {profit_color};'>₹{profit:,.2f}</div></div>", unsafe_allow_html=True)
            
    with tab2:
        st.markdown("### Setup Price Alerts")
        info_box("Get notified when prices reach your target.", "info")
        
        with st.form("alert_form"):
            ac_col1, ac_col2, ac_col3 = st.columns(3)
            with ac_col1:
                a_crop = st.selectbox("Crop", CROPS, key="alert_crop")
            with ac_col2:
                a_market = st.selectbox("Market", MARKETS["Maharashtra"], key="alert_market") # Simplified for demo
            with ac_col3:
                a_condition = st.selectbox("Condition", ["Goes Above", "Drops Below"])
                
            a_price = st.number_input("Target Price (₹)", min_value=100, value=2000)
            a_email = st.text_input("Email for Notification")
            
            submit_alert = st.form_submit_button("Save Alert")
            if submit_alert and a_email:
                save_alert(a_crop, a_market, a_price, a_condition, a_email)
                st.success(f"Alert saved! We will notify {a_email} when {a_crop} {a_condition.lower()} ₹{a_price} in {a_market}.")
                
        st.markdown("### Active Alerts")
        alerts = get_active_alerts()
        if alerts:
            df_alerts = pd.DataFrame(alerts, columns=["ID", "Crop", "Market", "Target Price", "Condition", "Email", "Status"])
            df_alerts["Status"] = "Active 🟢"
            st.dataframe(df_alerts.drop(columns=["ID"]), use_container_width=True, hide_index=True)
            
            if st.button("Trigger Demo Alert"):
                st.toast(f"🔔 ALERT: {alerts[-1][1]} in {alerts[-1][2]} just reached your target!", icon="🚨")
        else:
            st.info("No active alerts.")

if __name__ == "__main__":
    tools_page()
