import streamlit as st
from src.streamlit_side_navbar import render_sidebar

st.set_page_config(page_title="Company Profile", layout="wide")

render_sidebar()

query_params = st.query_params
ticker_symbol = query_params.get("ticker_symbol", None)

if st.button("← Back to Analysis"):
    st.switch_page("pages/2_market_analysis.py")

if ticker_symbol:
    st.subheader(f"🏢 {ticker_symbol} Profile")
    st.info(f"Fetching deep dive analysis for: **{ticker_symbol}**")
    
    # Here you would call your API/Database
    # data = get_stock_data(ticker)
    
    # Mock Data for demo
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Price", "₹2,450", "+1.2%")
    col2.metric("PE Ratio", "24.5", "-0.5")
    col3.metric("Sector", "Energy")
    
else:
    # st.error("No company selected. Please select a company from the Market Analysis page.")
    st.subheader(f"🏢 All Company Profile")