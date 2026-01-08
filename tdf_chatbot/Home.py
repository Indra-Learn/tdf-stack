import streamlit as st


# Configure the page settings (Global)
st.set_page_config(
    page_title="TheDataFestAI Smart Finance",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🦅 Welcome to TheDataFestAI Smart Finance")

# Simple State Management
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.warning("Please Login to access the Algo Dashboard.")
    if st.button("Log In (Simulation)"):
        st.session_state.logged_in = True
        st.success("Logged in! Check the sidebar for new pages.")
        st.rerun()
else:
    st.info("✅ System Status: ONLINE")
    st.write("Navigate to the **Dashboard** or **Algo Strategy** pages using the sidebar.")