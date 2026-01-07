"""
https://pypi.org/project/kiteconnect/

https://kite.trade/docs/connect/v3/
- https://kite.trade/docs/pykiteconnect/v4/
- https://github.com/zerodha/pykiteconnect
"""

import os
from dotenv import load_dotenv
import streamlit as st
from kiteconnect import KiteConnect

load_dotenv()

KITE_API_KEY = os.getenv("KITE_API_KEY")
KITE_API_SECRET = os.getenv("KITE_API_SECRET")

def kite_streamlit():
    if "kite" not in st.session_state:
        st.session_state.kite = None
    st.write("kite_streamlit Page")
    
    query_params = st.query_params
    request_token = query_params.get("request_token")

    if request_token:
        try:
            with st.spinner("Kite Connect Authenticating..."):
                # Initialize Kite
                kite = KiteConnect(api_key=KITE_API_KEY)

                # Exchange Request Token for Access Token
                data = kite.generate_session(request_token, api_secret=KITE_API_SECRET)
                kite.set_access_token(data["access_token"])

                # Store authenticated object in Session State
                st.session_state.kite = kite

                # CRITICAL: Clear the URL so we don't re-authenticate on refresh
                st.query_params.clear()
                st.rerun()

        except Exception as e:
            st.error(f"Login Failed: {e}")
            st.query_params.clear()

    if st.session_state.kite:
        # user is logged-in
        st.success("✅ Connected to Zerodha-Kite!")
        
        if st.button("Logout"):
            st.session_state.kite = None
            st.rerun()
        
        # Fetch User Profile
        st.json(st.session_state.kite.profile())
    else:
        # user is not logged-in
        st.warning("🔴 Disconnected from Zerodha-Kite!")

        # Generate the login link
        kite = KiteConnect(api_key=KITE_API_KEY)
        # login_url = kite.login_url()
        login_url = f"https://kite.zerodha.com/connect/login?api_key={KITE_API_KEY}"

        # Display the login button
        st.link_button("🔐 Login with Zerodha-Kite ", login_url)