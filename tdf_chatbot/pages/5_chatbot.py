import streamlit as st
from src.tdf_llm_apis import call_tdf_llm_apis
from src.streamlit_side_navbar import render_sidebar


st.set_page_config(page_title="ChatBot", layout="wide")

render_sidebar()

st.title("🦜🔗 TDF Applications - ")
st.markdown("---")
st.subheader("TDF ChatBot Interface")
st.write("Interact with the TDF ChatBot here.")
st.html("<h3>🚀 Get company and sector summaries using TDF API.</h3>")
input_company_ticker = st.text_input("Enter Company Ticker (e.g., Reliance, HDFC, SBI):")

if input_company_ticker:
    company_summary = call_tdf_llm_apis("company_summary", input_company_ticker)
    st.subheader("Company Summary")
    st.write(company_summary)

    sector_summary = call_tdf_llm_apis("sector_summary", input_company_ticker)
    st.subheader("Sector Summary")
    st.write(sector_summary)

    investment_summary = call_tdf_llm_apis("investment_recommendations", input_company_ticker)
    st.subheader("Investment Recommendations")
    st.write(investment_summary)

# if input_company_ticker:
#     if st.button("Get Company Summary"):
#         company_summary = get_company_summary(input_company_ticker)
#         st.subheader("Company Summary")
#         st.write(company_summary)
        
#     if st.button("Get Sector Summary"):
#         sector_summary = get_sector_summary(input_company_ticker)
#         st.subheader("Sector Summary")
#         st.write(sector_summary)