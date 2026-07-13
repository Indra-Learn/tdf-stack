import streamlit as st
import pandas as pd

st.header("Settings")
st.write(f"You are logged in as {st.session_state.role}.")