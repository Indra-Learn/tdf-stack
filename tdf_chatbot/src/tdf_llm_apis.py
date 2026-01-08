import requests


def call_tdf_llm_apis(endpoint: str, company_ticker: str) -> str:
    """
    Docstring for call_tdf_llm_apis
    
    :param endpoint: Description
    :type endpoint: str
    :param company_ticker: Description
    :type company_ticker: str
    :return: Description
    :rtype: str

    1. http://localhost:8000/company_summary
    2. http://localhost:8000/sector_summary
    3. http://localhost:8000/investment_recommendations
    """
    response = requests.post(f"http://72.61.231.147:8000/{endpoint}/invoke",
                             json={"input": {"company_ticker": company_ticker}}, verify=False)
    if response.status_code == 200:
        return response.json().get("output").get("content", 
                                                 "No data available for endpoint: {endpoint} and company: {company_ticker}.")
    else:
        return f"Error: {response.status_code} - {response.text}"