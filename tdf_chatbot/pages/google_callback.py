import streamlit as st
import time
import os
from authlib.integrations.requests_client import OAuth2Session
import extra_streamlit_components as stx
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Processing Login...", layout="centered")

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"

# 1. Get the Code
code = st.query_params.get("code")

if code:
    try:
        with st.spinner("Connecting to Google..."):
            # A. Exchange Code for Token
            oauth = OAuth2Session(CLIENT_ID, CLIENT_SECRET, redirect_uri=REDIRECT_URI)
            token = oauth.fetch_token(TOKEN_URL, authorization_response=st.query_params, code=code)
            
            # B. Get User Profile
            # Note: We use the session from fetch_token to make the request
            resp = oauth.get(USERINFO_URL)
            user_info = resp.json()
            
            # C. Save to Cookie (Persistent Login)
            cookie_manager = stx.CookieManager(key="callback_cookie_manager")
            cookie_manager.set("google_user_info", user_info, key="set_google_cookie")
            
            # D. Save to Session
            st.session_state["user_info"] = user_info
            
            st.success("Login Successful!")
            
            # E. Redirect to Home
            time.sleep(5) 
            st.switch_page("Home.py")
            
    except Exception as e:
        st.error(f"Login Failed: {e}")
        if st.button("Try Again"):
            st.switch_page("Home.py")
else:
    st.warning("No login code found.")
    if st.button("Go Home"):
        st.switch_page("Home.py")