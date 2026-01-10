import streamlit as st
from kiteconnect import KiteConnect
import os
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
KITE_API_KEY = os.getenv("KITE_API_KEY")
KITE_API_SECRET = os.getenv("KITE_API_SECRET")

st.set_page_config(page_title="Authenticating...", layout="centered")

# 2. Logic: Handle the Token
query_params = st.query_params
request_token = query_params.get("request_token")

if request_token:
    try:
        with st.spinner("Finalizing Login... Please wait."):
            # A. Initialize Kite
            kite = KiteConnect(api_key=KITE_API_KEY)

            # B. Exchange Token
            data = kite.generate_session(request_token, api_secret=KITE_API_SECRET)
            kite.set_access_token(data["access_token"])

            # C. Save to Session State (Shared across all pages)
            st.session_state["kite"] = kite
            
            # D. Success & Redirect Back
            st.success("Login Successful!")
            
            # This function automatically moves the user back to the Settings page
            # Make sure the filename matches exactly (case-sensitive)
            # st.query_params.clear()
            # st.rerun()
            st.switch_page("pages/6_settings.py") 

    except Exception as e:
        st.error(f"Authentication Failed: {e}")
        st.error("Please try logging in again from the Settings page.")
        if st.button("Back to Settings"):
            st.query_params.clear()
            st.switch_page("pages/6_settings.py")
else:
    st.warning("No token found. This page is for authentication callbacks only.")
    if st.button("Go to Settings"):
        st.query_params.clear()
        st.switch_page("pages/6_settings.py")