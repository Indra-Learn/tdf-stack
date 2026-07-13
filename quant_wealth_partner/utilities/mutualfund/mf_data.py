import os
import requests
import pandas as pd
import json
from datetime import datetime as dt, timedelta as td


base_dir = os.getcwd()

def get_mf_info():
    mf_info_path = os.path.join(base_dir, "utilities", "mutualfund", "mf_info.json")
    with open(mf_info_path, "r") as f:
        mf_info = json.load(f)
    return mf_info


amfi_base_url = "https://www.amfiindia.com/"
amfi_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Origin": "https://www.amfiindia.com",
    "Referer": "https://www.amfiindia.com/"
}

def amfi_api_call(full_url: str, payload: dict = {}, method: str = "GET", headers: dict = amfi_headers):
    """Generic function to make API calls to AMFI endpoints.
    Args:
        full_url (str): The complete URL for the API endpoint.
        payload (dict): The JSON payload to be sent in the POST request.
        method (str): The HTTP method to use for the request.
        headers (dict): The headers to be included in the request. Defaults to amfi_headers.
    Returns:
        dict: The JSON response from the API if the call is successful, None otherwise.
    """
    if method == "POST":
        response = requests.post(url=full_url, headers=headers, json=payload)
    else:
        response = requests.get(url=full_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"API call failed with status code: {response.status_code}")
        return None
    

def get_fund_performance_data():
    # fund_performance_web_url = "https://www.amfiindia.com/otherdata/fund-performance"
    is_holiday_api_url = "https://www.amfiindia.com/gateway/pollingsebi/api/amfi/isHoliday"
    fund_performance_filter_api_url = "https://www.amfiindia.com/gateway/pollingsebi/api/amfi/fundperformancefilters"
    fund_performance_subcategory_api_url = "https://www.amfiindia.com/gateway/pollingsebi/api/amfi/getsubcategory"
    fund_performance_api_url = "https://www.amfiindia.com/gateway/pollingsebi/api/amfi/fundperformance"

    fund_performance_filter_out = amfi_api_call(full_url=fund_performance_filter_api_url, payload={}, method="POST")
    final_output = fund_performance_filter_out.get("data")
    report_date = final_output.get("reportDate")

    df_maturity = pd.DataFrame(final_output.get('maturityTypeList')).rename(
        columns={'name': 'MaturityType_name', 'id': 'MaturityType_id'}
    )

    df_fund = pd.DataFrame(final_output.get('mutualFundList')).rename(
        columns={'name': 'MutualFund_name', 'id': 'MutualFund_id'}
    )

    investment_combined_dfs = []
    for category in final_output.get('investmentTypeList', []):
        # Using [category] instead of index=[0] is cleaner for dictionaries
        df_category = pd.DataFrame([category]).rename(
            columns={'name': 'InvestmentType_name', 'id': 'InvestmentType_id'}
        )

        # Make API Call for Subcategories
        fund_performance_subcategory_out = amfi_api_call(
            full_url=fund_performance_subcategory_api_url,
            payload={"category": category.get('id')},
            method="POST"
        )

        subcat_data = fund_performance_subcategory_out.get("data", [])

        if subcat_data:
            # If subcategories exist, create the dataframe and cross join with the parent category
            df_subcat = pd.DataFrame(subcat_data).rename(
                columns={'name': 'SubInvestmentType_name', 'id': 'SubInvestmentType_id'}
            )
            df_investment_segment = df_category.merge(df_subcat, how='cross')
            investment_combined_dfs.append(df_investment_segment)
        else:
            # If API returns no subcategories, safely keep the parent category with Null subcategories
            df_category['SubInvestmentType_name'] = pd.NA
            df_category['SubInvestmentType_id'] = pd.NA
            investment_combined_dfs.append(df_category)

    df_investment = pd.concat(investment_combined_dfs, ignore_index=True)

    df_final_fund_performance_filter = df_maturity.merge(df_investment, how='cross').merge(df_fund, how='cross')
    df_final_fund_performance_filter['ReportDate'] = final_output.get('reportDate')

    fund_performance_dfs = []

    for record in df_final_fund_performance_filter.loc[:,["MaturityType_name", "MaturityType_id", "InvestmentType_name", "InvestmentType_id", "SubInvestmentType_name", "SubInvestmentType_id", "ReportDate"]].drop_duplicates().itertuples(index=False):
        payload = dict()
        payload["maturityType"] = record.MaturityType_id
        payload["category"] = record.InvestmentType_id
        payload["subCategory"] = record.SubInvestmentType_id
        payload["mfid"] = 0
        payload["reportDate"] = record.ReportDate

        fund_performance_out = amfi_api_call(full_url=fund_performance_api_url, payload=payload, method="POST")
        fund_performance_df = pd.DataFrame(fund_performance_out.get("data"))

        if fund_performance_df.empty:
            continue
        fund_performance_df['maturity_type'] = record.MaturityType_name
        fund_performance_df['investment_type'] = record.InvestmentType_name
        fund_performance_df['sub_category'] = record.SubInvestmentType_name
        fund_performance_dfs.append(fund_performance_df)
        # print(f"Payload: {payload}")
    final_fund_performance_df = pd.concat(fund_performance_dfs, ignore_index=True)
    final_fund_performance_df = final_fund_performance_df.loc[:, ['preNavDate', 'preNavRegular', 'preNavDirect', 'schemeName', 'benchmark', 
        'riskometerScheme',     'riskometerBenchmark','navDate', 'navDirect',
        'return7DaysDirect', 'return7DaysBenchmark', 'return15DaysDirect', 'return15DaysBenchmark',
        'return1MonthDirect', 'return1MonthBenchmark', 'return3MonthDirect', 'return3MonthBenchmark',
        'return6MonthDirect', 'return6MonthBenchmark', 'return1YearDirect', 'return1YearBenchmark',
        'return3YearDirect', 'return3YearBenchmark', 'return5YearDirect', 'return5YearBenchmark',
        'return10YearDirect', 'return10YearBenchmark', 'returnSinceLaunchDirect', 'returnSinceLaunchBenchmarkDirect',
        'dailyAUM', 'preMonthAUM', 'preMonthAvgAUM', 'ir1YrDirect', 'ir3YrDirect', 'ir5YrDirect', 'ir10YrDirect', 'maturity_type', 'investment_type', 'sub_category']]
    return final_fund_performance_df