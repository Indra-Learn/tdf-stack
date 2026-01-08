import streamlit as st


st.set_page_config(page_title="Overview", layout="wide")

st.subheader("Welcome to TheDataFestAI Smart Finance App")
st.write("Here is your multiple investment options")

col1, col2, col3 = st.columns(3)
# col1.metric("Revenue", "$50,000", "+5%")
# col2.metric("Users", "1,200", "-2%")
# col3.metric("Uptime", "99.9%", "0%")
col1.caption("India Equity")
col2.caption("US Equity")
col3.caption("Real Estate")


col1, col2, col3 = st.columns(3)
col1.caption("Crypto")
col2.caption("Bonds")
col3.caption("Gold/Silver")