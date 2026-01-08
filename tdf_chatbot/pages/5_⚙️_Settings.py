import streamlit as st


st.set_page_config(page_title="Settings", layout="wide")

st.subheader("User Settings")
st.checkbox("Enable Dark Mode")
st.checkbox("Show Notifications")