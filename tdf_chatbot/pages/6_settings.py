import os
import streamlit as st
from kiteconnect import KiteConnect
from dotenv import load_dotenv
from src.streamlit_side_navbar import render_sidebar

load_dotenv()

KITE_API_KEY = os.getenv("KITE_API_KEY")

st.set_page_config(page_title="Settings", layout="wide")

render_sidebar()

if "kite" not in st.session_state:
    st.session_state.kite = None

st.subheader("User Settings -")

# st.caption("Connect To INDMoney")

with st.container(border=True):
    col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
    is_connected = st.session_state.kite is not None
    with col1:
        if is_connected:
            st.markdown("### ✅")
        else:
            st.markdown("### ❌")

    with col2:
        st.markdown("## Zerodha-Kite")

    with col3:
        if is_connected:
            st.caption("Status: **Connected**")
            st.caption("Token Valid")
        else:
            st.caption("Status: **Disconnected**")
            st.caption("Action Required")

    with col4:
        if is_connected:
            # If connected, show Logout
            if st.button("Unlink Account"):
                st.session_state.kite = None
                st.rerun()
        else:
            # If disconnected, show Login Link
            try:
                kite = KiteConnect(api_key=KITE_API_KEY)
                # login_url = kite.login_url()
                login_url = f"https://kite.zerodha.com/connect/login?api_key={KITE_API_KEY}"
                st.link_button("🔐 Login to Kite", login_url, type="primary")
            except Exception:
                st.error("API Key Missing")

