import requests
import streamlit as st

def get_company_summary(company_ticker: str) -> str:
    response = requests.post("http://72.61.231.147:8000/company_summary/invoke",
                             json={"input": {"company_ticker": company_ticker}})
    if response.status_code == 200:
        return response.json().get("output").get("content", "No summary available.")
    else:
        return f"Error: {response.status_code} - {response.text}"
    
def get_sector_summary(company_ticker: str) -> str:
    response = requests.post("http://72.61.231.147:8000/sector_summary/invoke",
                             json={"input": {"company_ticker": company_ticker}})
    if response.status_code == 200:
        return response.json().get("output").get("content", "No summary available.")
    else:
        return f"Error: {response.status_code} - {response.text}"
    
st.title("🦜🔗 TDF ChatBot - ")
st.html("<h3>🚀 Get company and sector summaries using TDF API.</h3>")
input_company_ticker = st.text_input("Enter Company Ticker (e.g., Reliance, HDFC, SBI):")

if input_company_ticker:
    company_summary = get_company_summary(input_company_ticker)
    st.subheader("Company Summary")
    st.write(company_summary)
    
    sector_summary = get_sector_summary(input_company_ticker)
    st.subheader("Sector Summary")
    st.write(sector_summary)


# if input_company_ticker:
#     if st.button("Get Company Summary"):
#         company_summary = get_company_summary(input_company_ticker)
#         st.subheader("Company Summary")
#         st.write(company_summary)
        
#     if st.button("Get Sector Summary"):
#         sector_summary = get_sector_summary(input_company_ticker)
#         st.subheader("Sector Summary")
#         st.write(sector_summary)