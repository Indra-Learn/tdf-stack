import streamlit as st
from src.kite_connect import kite_portfolio
from src.streamlit_side_navbar import render_sidebar


st.set_page_config(page_title="Portfolio Tracker", layout="wide")

render_sidebar()
if not st.user.is_logged_in:
    st.error("You do not have permission to view this page. Please log in from the home page.")
    st.stop() 

if "kite" not in st.session_state:
    st.session_state.kite = None

st.subheader("🪁 TheDataFestAI - Portfolio Tracker")
st.write("Track your investment portfolio here.")
st.markdown("---")

if st.session_state.kite:
    kite = st.session_state.kite
    st.html("<h4>User Portfolio</h4>")
    st.dataframe(kite_portfolio(kite.holdings()))
    # st.json(kite.holdings())
else:
    st.html("<h4>Visit to <b>Setting</b> to connect to Zerodha-Kite</h4>")
