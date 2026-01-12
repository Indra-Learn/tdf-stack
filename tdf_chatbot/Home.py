import streamlit as st
from src.streamlit_side_navbar import render_sidebar
from src.google_auth import login_button, get_current_user, logout


# Configure the page settings (Global)
st.set_page_config(
    page_title="TheDataFestAI Smart Finance",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "user_info" not in st.session_state:
    st.session_state["user_info"] = None

st.title("🦅 Welcome to TheDataFestAI Smart Finance")

# user = get_current_user()

# if not user:
#     # --- LOGGED OUT STATE ---
#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         st.title("🔒 Login Required")
#         st.write("Welcome to the Algo Platform. Please verify your identity.")
#         login_button() # Shows the Google Button
#     st.stop()

# --- LOGGED IN STATE ---
render_sidebar()

# st.title(f"Welcome, {user.get('name')}")
# st.write(f"Logged in as: *{user.get('email')}*")

# if st.button("Logout"):
#     logout()

