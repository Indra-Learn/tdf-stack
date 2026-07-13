import streamlit as st

def render_sidebar():
    is_disabled = True
    with st.sidebar:
        st.subheader("🧠   TheDataFestAI (TDF)")
        st.markdown("---")
        if st.user.is_logged_in:
            st.html(f"Hello, <span style='color: orange; font-weight: bold;'>{st.user.name}</span>")
            is_disabled = False
        else:
            st.html("Hello, <span style='color: orange; font-weight: bold;'>Guest User</span>!")
        st.page_link("Home.py", label="Login / Logout")
        st.divider()
        # Manually list ONLY the pages you want the user to see
        st.page_link("Home.py", label="Home", icon="🏠")
        st.page_link("pages/1_overview.py", label="Overview", icon="🖐")
        st.page_link("pages/2_market_analysis.py", label="Market Analysis", icon="📊")
        st.page_link("pages/3_company_profile.py", label="Company Profile", icon="💼")
        st.page_link("pages/4_portfolio_tracker.py", label="Portfolio Tracker", icon="💰", disabled=is_disabled)
        st.page_link("pages/5_chatbot.py", label="ChatBot", icon="💬", disabled=is_disabled)
        st.page_link("pages/9_stock_market_fundamentals.py", label="Market Fundamentals", icon="🦚")
        st.page_link("pages/8_swing_trading.py", label="Swing Trading", icon="🏆")
        st.page_link("pages/10_Mahesh_Kaushik_Strategy.py", label="Mahesh Kaushik Sir Strategies", icon="🏆")
        st.page_link("pages/11_mutual_fund.py", label="Mutual Funds", icon="💰")
        st.page_link("pages/6_settings.py", label="Settings", icon="🛠", disabled=is_disabled)
        st.page_link("pages/7_about_us.py", label="About_Us", icon="📣")
        
        
        # Note: We purposely do NOT add 'kite_redirect.py' here.
        # It still exists as a valid URL, but no button will appear for it.