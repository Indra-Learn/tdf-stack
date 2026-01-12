import os
import time
import streamlit as st
import extra_streamlit_components as stx
from authlib.integrations.requests_client import OAuth2Session
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET") # Check typo in env var name usually used
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

# Google's Standard Endpoints
AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"
SCOPE = "openid email profile"

def get_cookie_manager():
    # Use a unique key to avoid re-initializing
    return stx.CookieManager(key="google_auth_cookies")

def login_button():
    """Generates the Google Login Link"""
    if not CLIENT_ID or not CLIENT_SECRET:
        st.error("Missing Google Credentials in .env file")
        return

    oauth = OAuth2Session(CLIENT_ID, CLIENT_SECRET, scope=SCOPE, redirect_uri=REDIRECT_URI)
    uri, state = oauth.create_authorization_url(AUTHORIZATION_BASE_URL)
    
    # Custom Google Sign-In Button Styling
    # st.markdown(f'''
    #     <a href="{uri}" target="_self">
    #         <button style="
    #             background-color: #ffffff; color: #3c4043; 
    #             border: 1px solid #dadce0; border-radius: 4px;
    #             padding: 10px 15px; font-family: 'Google Sans', arial, sans-serif; 
    #             font-size: 14px; font-weight: 500; cursor: pointer; 
    #             display: flex; align-items: center; gap: 10px;">
    #             <img src="https://lh3.googleusercontent.com/COxitqgJr1sJnIDe8-jiKhxDx1FrYbtRHKJ9z_hELisAlapwE9LUPh6fcXIfb5vwpbMl4xl9H9TRFPc5NOO8Sb3VSgIBrfRYvW6cUA" width="18" height="18">
    #             Sign in with Google
    #         </button>
    #     </a>
    # ''', unsafe_allow_html=True)
    st.link_button("Sign in with Google", uri, type="primary", use_container_width=True)


def get_current_user():
    """
    Checks if user is logged in via Cookies or Session.
    """
    # 1. Check Session (Fastest)
    # if "user_info" in st.session_state and st.session_state.user_info:
    if "user_info" in st.session_state:
        return st.session_state.user_info

    # 2. Check Cookie (Persistence)
    cookie_manager = get_cookie_manager()
    user_data = cookie_manager.get("google_user_info")
    if user_data:
        st.session_state.user_info = user_data
        return user_data
    return None


def logout():
    cookie_manager = get_cookie_manager()
    cookie_manager.delete("google_user_info")
    st.session_state.user_info = None
    time.sleep(5)
    st.rerun()