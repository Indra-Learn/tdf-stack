import streamlit as st
from streamlit_extras.steps import steps
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Atlanta Apartment: Financial Health Dashboard")

# Top Level Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.subheader("Total Wealth")
    st.markdown("<h2 style='color: #1E88E5;'>₹1.50 Cr</h2>", unsafe_allow_html=True)
    st.caption("Total Assets")

with col2:
    st.subheader("Safe Reserves")
    st.markdown("<h2 style='color: #43A047;'>₹99.63 L</h2>", unsafe_allow_html=True)
    st.caption("Fixed Deposits")

with col3:
    st.subheader("This Year's Surplus")
    st.markdown("<h2 style='color: #43A047;'>₹19.59 L</h2>", unsafe_allow_html=True)
    st.caption("Profit / Loss A/c (Current Period)")

with col4:
    st.subheader("Unpaid Maintenance")
    # Emphasizing the risk directly in the markdown color
    st.markdown("<h2 style='color: #E53935;'>₹45.00 L</h2>", unsafe_allow_html=True)
    st.caption("Sundry Debtors (ACTION REQUIRED)")

st.divider()

# Visual Asset Distribution
st.subheader("Where is our money currently sitting?")

# Structuring the balance sheet assets for a non-financial breakdown
data = {
    "Asset Category": ["Fixed Deposits (Safe)", "Unpaid Dues (At Risk)", "Bank Balance (Liquid)", "Accrued Interest & TDS"],
    "Amount (₹)": [9963086, 4500000, 253796, 308205] 
}
df = pd.DataFrame(data)

# Donut chart for clean, proportional visualization
fig = px.pie(
    df, 
    values="Amount (₹)", 
    names="Asset Category", 
    color="Asset Category",
    color_discrete_map={
        "Fixed Deposits (Safe)": "#4CAF50",      # Green
        "Unpaid Dues (At Risk)": "#F44336",      # Red
        "Bank Balance (Liquid)": "#2196F3",      # Blue
        "Accrued Interest & TDS": "#9E9E9E"      # Grey
    },
    hole=0.4
)

fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig, width='stretch')