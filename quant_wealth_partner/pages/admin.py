import streamlit as st
import time

st.header("Admin Dashboard")

with st.sidebar:
    with st.echo():
        st.write("This is the sidebar")

    with st.spinner("Loading..."):
        time.sleep(5)
    st.success("Done!")