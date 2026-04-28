import streamlit as st
from datetime import date

# App Config
st.set_page_config(
    page_title="KisanMitra - AI Farm Intelligence",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main app logic
def main():
    # Sidebar
    with st.sidebar:
        st.markdown("<h1 style='font-family:Georgia,serif;'>🌾 KisanMitra</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:1.1rem; opacity:0.9;'>AI Farm Intelligence Platform</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.write(f"**Today:** {date.today().strftime('%B %d, %Y')}")
        st.markdown("---")
        
        st.markdown("### Quick Stats")
        st.markdown("🌱 **Crops Monitored:** 10+")
        st.markdown("📍 **Markets Tracked:** 30+")
        st.markdown("🤖 **AI Models:** Prophet, LSTM, XGBoost")
        
        st.markdown("---")
        st.markdown("""
        <div style='background-color: rgba(0,0,0,0.2); padding: 10px; border-radius: 5px; font-size: 0.8rem;'>
            <i>Disclaimer: AI predictions are estimates based on historical data. Market conditions may vary.</i>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div style='text-align: center; padding: 2rem;'>
            <h1 style='color: #1b4332; font-family: Georgia, serif;'>Welcome to KisanMitra</h1>
            <p style='font-size: 1.2rem; color: #333;'>Select a module from the sidebar to get started.</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()