import streamlit as st
from src.streamlit_side_navbar import render_sidebar
from src.mutual_fund_india.mf import get_amfi_fund_performance, get_amfi_category_subcategory


st.set_page_config(page_title="Mutual Funds", layout="wide")

render_sidebar()

# if "scheme_df" not in st.session_state:
#     st.session_state.scheme_df = get_schemes()
# scheme_df = st.session_state.scheme_df

if "amfi_fund_performance" not in st.session_state:
    st.session_state.amfi_fund_performance = get_amfi_fund_performance()
amfi_fund_performance_df = st.session_state.amfi_fund_performance

# st.subheader("About Mutual Funds -")
# st.dataframe(scheme_df)

st.subheader("Category & Subcategory -")
st.dataframe(get_amfi_category_subcategory())

st.subheader("AMFI Fund Performance -")
st.dataframe(amfi_fund_performance_df)