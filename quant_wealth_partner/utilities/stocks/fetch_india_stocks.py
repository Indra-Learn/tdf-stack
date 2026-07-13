import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
import pytz
import time
import json

base_nse_url = "https://www.nseindia.com"
nse_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


# common nse api fetch functionality
@st.cache_resource
def nse_fetch_data(nse_url: str) -> dict:
    """
    Fetch data from NSE API.

    :param nse_url: URL for the NSE API endpoint
    :type nse_url: str

    :return: JSON response from the NSE API
    :rtype: dict
    """
    try:
        nse_session = requests.Session()
        nse_session.headers.update(nse_headers)
        nse_session.get(base_nse_url, headers=nse_headers,  timeout=10)
        nse_session.get(base_nse_url+"/option-chain", headers=nse_headers,  timeout=10)

        full_nse_api_url = base_nse_url + nse_url
        # print(f"calling {full_nse_api_url} ..")

        response = nse_session.get(full_nse_api_url)
        response.raise_for_status()

        print(f"Successfully fetched data from {full_nse_api_url}")
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching data from NSE API: {e}")
        return {"error": f"{e}"}
    

# index_category_list_api_url = "/api/heatmap-index-catergory-list"

# index_category_list = nse_fetch_data(index_category_list_api_url)

# # index_category_list
# # ['Broad Market Indices', 'Sectoral Indices', 'Thematic Indices', 'Strategy Indices']

# broad_market_indices_api_url = "/api/heatmap-index?type=Broad%20Market%20Indices"
# broad_market_indices_heatmap_data = nse_fetch_data(broad_market_indices_api_url)
# broad_market_indices_heatmap_df = pd.DataFrame(broad_market_indices_heatmap_data)

# broad_market_indices_heatmap_df = broad_market_indices_heatmap_df.loc[:, ["index", "indexLongName", "open", "high", "low", "close", "current", "pChange", "yrHigh", "yrLow", "timeStamp"]]

# # broad_market_indices_heatmap_df

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_all_indices_data() -> pd.DataFrame:
    """
    Fetch all indices data from NSE API.

    :return: DataFrame containing all indices data
    :rtype: pd.DataFrame
    """
    all_indices_api_url = "/api/allIndices"
    try:
        all_indices_data = nse_fetch_data(all_indices_api_url)
    except Exception as e:
        print(f"Error fetching data from NSE API: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

    all_indices_df = pd.DataFrame(all_indices_data.get("data", []))
    return all_indices_df

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_market_watch_index_data(selected_index: str) -> pd.DataFrame:
    """
    Fetch market watch index data for a specific index from NSE API.

    :param selected_index: The index for which to fetch market watch data
    :type selected_index: str

    :return: DataFrame containing market watch index data
    :rtype: pd.DataFrame
    """

    market_watch_index_api_url = f"/api/NextApi/apiClient/marketWatchApi?functionName=getIndicesData&symbol={selected_index}"
    indices_return_api_url = f"/api/NextApi/apiClient/indexTrackerApi?functionName=getIndicesReturn&&index={selected_index}"
    indices_heatmap_api_url = f"/api/NextApi/apiClient/indexTrackerApi?functionName=getIndicesHeatMap&&index={selected_index}"

    market_watch_index_data = nse_fetch_data(market_watch_index_api_url)
    market_watch_index_df = pd.DataFrame(market_watch_index_data.get("data", {}).get("data", []))  #marketStatus, #aduCount

    indices_heatmap_data = nse_fetch_data(indices_heatmap_api_url)

    indices_heatmap_df = pd.DataFrame(indices_heatmap_data.get("data", []))

    if not market_watch_index_df.empty:
        market_watch_index_df['Volume'] = round(market_watch_index_df['totalTradedVolume'].astype(float) / 100000, 2)  #in lakhs
        market_watch_index_df['TradedValue'] = round(market_watch_index_df['totalTradedValue'].astype(float) / 10000000, 2)  #in crores
        market_watch_index_df['Floating_MCap'] = round(market_watch_index_df['ffmc'].astype(float) / 10000000, 2)  #in crores

    final_df = pd.merge(market_watch_index_df, indices_heatmap_df[['symbol', 'VWAP']], how='left', left_on='symbol', right_on='symbol')

    return final_df.loc[final_df['priority'] == 0, ['companyName', 'symbol', 'series', 'open', 'dayHigh', 'dayLow', 'lastPrice', 'change', 'pChange', 'VWAP', 'previousClose', 
                                         'Volume', 'TradedValue', 'Floating_MCap', 'yearHigh', 'yearLow', 'perChange30d', 'perChange365d']]


# https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getAllIndices
# https://www.nseindia.com/api/NextApi/apiClient?functionName=getGiftNifty

# https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getIndexData&&index=NIFTY%2050
# https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getAdvanceDecline&&index=NIFTY%2050
# https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getAllIndicesSymbols&&index=NIFTY%2050
# https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getTopFiveStock&&flag=G&&index=NIFTY%2050
# https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getContributionData&&index=NIFTY%2050&&noofrecords=0&&flag=1
# https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getContributionData&&index=NIFTY%2050&&flag=0
# imp: https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getIndicesHeatMap&&index=NIFTY%2050
# imp: https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getConstituents&&index=NIFTY%2050&&noofrecords=0
# https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getConstituents&&index=NIFTY%2050&&noofrecords=7
# imp: https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getCorporateAction&&flag=CAC&&index=NIFTY%2050
# https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getMostActiveContracts&&index=NIFTY
# AI USECASE: https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getAnnouncementsIndices&flag=CAN&&index=NIFTY%2050
# https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getBoardMeeting&&flag=BM&&index=NIFTY%2050
# https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getIndexFacts&&index=NIFTY%2050

# https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getShareHoldingData&&symbol=ADANIENT
# https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getFinancialResultGraph&&symbol=ADANIENT
# https://www.nseindia.com/api/equity-metainfo?symbol=ADANIENT
# https://www.nseindia.com/api/corporate-share-holdings-master?index=equities&symbol=ADANIENT
# https://www.nseindia.com/api/corporate-share-holdings-master?index=sme&symbol=ADANIENT

# https://www.nseindia.com/api/holiday-master?type=trading

# https://www.nseindia.com/api/corpreg7?index=sme
# https://www.nseindia.com/api/corpreg7?index=equities