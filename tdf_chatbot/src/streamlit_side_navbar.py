import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.subheader("🧠   TheDataFestAI (TDF)")
        st.markdown("---")
        # Manually list ONLY the pages you want the user to see
        st.page_link("Home.py", label="Home", icon="🏠")
        st.page_link("pages/1_overview.py", label="Overview", icon="🖐")
        st.page_link("pages/2_market_analysis.py", label="Market Analysis", icon="📊")
        st.page_link("pages/3_portfolio_tracker.py", label="Portfolio Tracker", icon="💰")
        st.page_link("pages/4_company_profile.py", label="Company Profile", icon="💼")
        st.page_link("pages/5_chatbot.py", label="ChatBot", icon="💬")
        st.page_link("pages/6_settings.py", label="Settings", icon="🛠")
        st.page_link("pages/7_about_us.py", label="About_Us", icon="📣")
        
        
        # Note: We purposely do NOT add 'kite_redirect.py' here.
        # It still exists as a valid URL, but no button will appear for it.