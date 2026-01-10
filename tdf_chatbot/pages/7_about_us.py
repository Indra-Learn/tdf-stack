import streamlit as st
from src.streamlit_side_navbar import render_sidebar


st.set_page_config(page_title="About Us", layout="wide")

render_sidebar()

st.subheader("About TheDataFestAI App -")

st.write("Hey Folks, ")
st.write("We are thrilled to announce that we have started working to build/develop a well investment screening platform.")
st.write("So that, you can choose right investment path and make investment decession based on data, not by emotion")