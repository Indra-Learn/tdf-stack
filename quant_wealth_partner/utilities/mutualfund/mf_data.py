import os
import json
import requests
import pandas as pd
import json
from datetime import datetime as dt, timedelta as td
import time
# from mftool import Mftool

# current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.getcwd()

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




amfi_base_url = "https://www.amfiindia.com/"
amfi_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Origin": "https://www.amfiindia.com",
    "Referer": "https://www.amfiindia.com/"
}

def get_mf_info():
    mf_info_path = os.path.join(base_dir, "utilities", "mutualfund", "mf_info.json")
    with open(mf_info_path, "r") as f:
        mf_info = json.load(f)
    return mf_info


def get_amfi_group_companies():
    page = 1
    pageSize = 30
    full_url = amfi_base_url + f"api/list-of-all-group-companies?page={page}&pageSize={pageSize}"
    try:
        response = requests.get(full_url, headers=amfi_headers)
        all_data = response.json().get("data", [])
        to_range = int(response.json().get("pagination").get("pageCount")) + 1
        for i in range(2, to_range):
            full_url = amfi_base_url + f"api/list-of-all-group-companies?page={i}&pageSize={pageSize}"
            response = requests.get(full_url, headers=amfi_headers)
            all_data.extend(response.json().get("data"))
        df = pd.DataFrame(all_data)
        return df
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False


def get_amfi_category_subcategory():
    # https://www.amfiindia.com/api/latest-nav-category?mfid=all&type=

    full_url = amfi_base_url + "gateway/pollingsebi/api/amfi/getsubcategory"
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


def get_amfi_mutual_fund_id():
    # https://www.amfiindia.com/api/amc-adresses?page=1&pageSize=12&MF_ID=53
    # https://www.amfiindia.com/api/amc-adresses?page=1&pageSize=12
    # https://www.amfiindia.com/api/amc-adresses?page=1&pageSize=12&MF_ID=53&City=ETAWAH
    full_url = amfi_base_url + f"api/amc-adresses?page=1&pageSize=1"
    try:
        response = requests.get(full_url, headers=amfi_headers)
        data = response.json().get("amcs")
        df = pd.DataFrame(data)
        return df
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False

def get_amfi_mutual_fund_scheme(mf_id):
    full_url = amfi_base_url + f"api/populate-scheme?MF_ID={mf_id}"
    try:
        response = requests.get(full_url, headers=amfi_headers)
        data = response.json()
        df = pd.DataFrame(data)
        return df
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False


def get_amfi_all_mutual_fund_schemes():
    dfs = []
    amfi_mutual_fund_id_df = get_amfi_mutual_fund_id()
    for row in amfi_mutual_fund_id_df.itertuples(index=True, name='Pandas'):
        # print(row.Index, row.mf_id)
        df = get_amfi_mutual_fund_scheme(mf_id=48)
        dfs.append(df)
    final_df = pd.concat(dfs, ignore_index=True)
    return final_df

def get_amfi_fund_performance(maturityType=1, category=1, subCategory=1, mfid=0, reportDate="27-Mar-2026"):
    full_url = amfi_base_url + "gateway/pollingsebi/api/amfi/fundperformance"
    payload = {
        "maturityType": maturityType,
        "category": category,
        "subCategory": subCategory,
        "mfid": mfid,
        "reportDate": reportDate
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
    

if __name__ == "__main__":
    amfi_category_subcategory_df = get_amfi_category_subcategory()
    print(amfi_category_subcategory_df.head())