import streamlit as st
from src.streamlit_side_navbar import render_sidebar

st.set_page_config(page_title="Market Analysis", layout="wide")

render_sidebar()

st.subheader("🎯 Swing Trading Concepts & Fundamentals")
st.write("🙏 Thanks to Mahesh Kaushik Sir")

stock_market_foundation_list = [
    {
        "concept": "Darvas Theory",
        "logic": []
    },
    {
        "concept": "Munehisa Homma",
        "logic": ["Monitor Candlestick Pattern for 3 consecutive monthly/weekly data"]
    },
]

for item in stock_market_foundation_list:
    # Create a clickable card for each concept
    with st.expander(f"📘 {item['concept']}"):
        if item["logic"]:
            st.markdown("**Core Logic:**")
            # Render the list as clean bullet points
            for point in item["logic"]:
                st.markdown(f"- {point}")
        else:
            st.info("No specific logic defined for this module yet.")