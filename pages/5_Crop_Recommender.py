import streamlit as st
import random
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.ui_helpers import page_header

st.set_page_config(page_title="Recommender - KisanMitra", page_icon="🌾", layout="wide")

def get_recommendations(state, month, acres, budget):
    """Mock ML logic for crop recommendations based on rules."""
    all_recs = [
        {"crop": "Tomato", "emoji": "🍅", "price": 1800, "cost_per_acre": 25000, "yield_per_acre": 150, "season": "Kharif/Rabi"},
        {"crop": "Onion", "emoji": "🧅", "price": 1200, "cost_per_acre": 20000, "yield_per_acre": 120, "season": "Rabi"},
        {"crop": "Wheat", "emoji": "🌾", "price": 2200, "cost_per_acre": 15000, "yield_per_acre": 20, "season": "Rabi"},
        {"crop": "Soybean", "emoji": "🌿", "price": 4600, "cost_per_acre": 18000, "yield_per_acre": 10, "season": "Kharif"},
        {"crop": "Cotton", "emoji": "☁️", "price": 6200, "cost_per_acre": 30000, "yield_per_acre": 8, "season": "Kharif"}
    ]
    
    # Filter by budget
    valid_recs = [r for r in all_recs if r["cost_per_acre"] * acres <= budget]
    if not valid_recs:
        return []
    
    # Shuffle for variety
    random.shuffle(valid_recs)
    return valid_recs[:3]

def crop_recommender():
    page_header("🌾", "Crop Recommender", "Find the best crops for your farm")
    
    with st.form("recommender_form"):
        col1, col2 = st.columns(2)
        with col1:
            state = st.selectbox("State", ["Maharashtra", "Karnataka", "Punjab", "UP"])
            district = st.text_input("District", value="Pune")
        with col2:
            month = st.selectbox("Planting Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], index=5)
            acres = st.number_input("Farm Size (Acres)", min_value=1.0, value=5.0, step=0.5)
            budget = st.number_input("Budget (₹)", min_value=10000, value=150000, step=10000)
            
        submitted = st.form_submit_button("Get Recommendations")
        
    if submitted:
        recs = get_recommendations(state, month, acres, budget)
        
        if not recs:
            st.error("Your budget is too low for the selected farm size. Please increase budget or reduce acres.")
            return
            
        st.markdown(f"### Top 3 Recommendations for {acres} Acres in {state}")
        
        cols = st.columns(len(recs))
        for i, rec in enumerate(recs):
            with cols[i]:
                revenue = rec["price"] * rec["yield_per_acre"] * acres
                cost = rec["cost_per_acre"] * acres
                profit = revenue - cost
                
                card_html = f"""
<div style="background-color: white; border: 1px solid #74c69d; border-radius: 12px; padding: 1.5rem; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05); transition: transform 0.2s;">
    <div style="font-size: 3rem; margin-bottom: 0.5rem;">{rec["emoji"]}</div>
    <h3 style="color: #1b4332; margin-top: 0;">{rec["crop"]}</h3>
    <div style="background-color: #f5f0e8; padding: 0.5rem; border-radius: 4px; font-size: 0.8rem; margin-bottom: 1rem; color: #333;">
        <strong>Season:</strong> {rec["season"]}
    </div>
    <p style="margin: 0.2rem 0; color: #555;">Expected Price: <strong>₹{rec["price"]}/Q</strong></p>
    <p style="margin: 0.2rem 0; color: #555;">Est. Yield: <strong>{rec["yield_per_acre"] * acres:.0f} Q</strong></p>
    <p style="margin: 0.2rem 0; color: #555;">Total Cost: <strong>₹{cost:,.0f}</strong></p>
    <hr style="border: none; border-top: 1px solid #eee; margin: 1rem 0;">
    <div style="color: #2d6a4f; font-weight: bold; font-size: 1.2rem;">
        Est. Profit: ₹{profit:,.0f}
    </div>
</div>
"""
                st.markdown(card_html, unsafe_allow_html=True)

if __name__ == "__main__":
    crop_recommender()
