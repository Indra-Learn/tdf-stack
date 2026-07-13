import requests
import pandas as pd
import json
import datetime
from mftool import Mftool


# mf_obj = Mftool()

# def get_schemes():
#     scheme_codes = []
#     scheme_names = []
#     scheme_aum = []
    
#     schemes_dict = mf_obj.get_scheme_codes()
#     for i, (key, value) in enumerate(schemes_dict.items()):
#         if i == 0:
#             continue
#         scheme_codes.append(key)
#         scheme_names.append(value)
#         scheme_aum.append(value.split('-')[0])
#     schemes_df = pd.DataFrame({"Scheme Code": scheme_codes, 
#                             "Scheme Name": scheme_names, 
#                             "Scheme AUM": scheme_aum})
#     return schemes_df




amfi_base_url = "https://www.amfiindia.com/gateway/pollingsebi/api/"
amfi_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Origin": "https://www.amfiindia.com",
    "Referer": "https://www.amfiindia.com/"
}

def get_amfi_category_subcategory():
    full_url = amfi_base_url + "amfi/getsubcategory"
    # maturityType = {"Open Ended": 1, "Close Ended": 2}
    categories = {"Equity": 1, "Debt": 2, "Hybrid": 3, "Solution Oriented": 4, "Other": 5}
    try:
        df_list = []
        for category_name, category_id in categories.items():
            payload = {
                "category": category_id
            }
            response = requests.post(url=full_url, 
                                    headers=amfi_headers, 
                                    json=payload)
            response.raise_for_status()
            data = response.json().get("data", [])
            # No data found for category:
            if not data:
                continue
            df = pd.DataFrame(data)
            df.rename(columns={"name": "sub_category_name", "id": "sub_category_id"}, inplace=True)
            df["category_id"] = category_id
            df["category_name"] = category_name
            df_list.append(df.loc[:,["category_name", "category_id", "sub_category_name", "sub_category_id"]])
        final_df = pd.concat(df_list, ignore_index=True)
        return final_df
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False
    
def get_amfi_fund_performance():
    full_url = amfi_base_url + "amfi/fundperformance"
    payload = {
        "maturityType":1,
        "category":1,
        "subCategory":1,
        "mfid":0,
        "reportDate":"27-Mar-2026"
    }
    try:
        response = requests.post(url=full_url, 
                                headers=amfi_headers, 
                                json=payload)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data.get("data"))
        return df
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False