import streamlit as st
from src.kite_connect import kite_streamlit


st.set_page_config(page_title="Portfolio Tracker", layout="wide")

st.title("🪁 TheDataFestAI - Portfolio Tracker")
st.write("Track your investment portfolio here.")
st.markdown("---")
kite_streamlit()