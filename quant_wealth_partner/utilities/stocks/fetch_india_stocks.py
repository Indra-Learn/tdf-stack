import streamlit as st
import requests
import pandas as pd
import numpy as np
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
import pytz
import time
import json
import aiohttp
import asyncio
from io import StringIO


# common nse api fetch functionality
@st.cache_resource
def nse_fetch_data(nse_url: str, method: str = "GET", payload: dict = {}) -> dict:
    """
    Fetch data from NSE API.

    :param nse_url: URL for the NSE API endpoint
    :type nse_url: str

    :param method: GET/POST method for the NSE API endpoint
    :type method: str

    :param payload: Payload for POST method for the NSE API endpoint
    :type payload: dict

    :return: JSON response from the NSE API
    :rtype: dict
    """
    base_nse_url = "https://www.nseindia.com"
    nse_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        nse_session = requests.Session()
        nse_session.headers.update(nse_headers)
        nse_session.get(base_nse_url, headers=nse_headers,  timeout=10)
        nse_session.get(base_nse_url+"/option-chain", headers=nse_headers,  timeout=10)

        if method == "GET":
            response = nse_session.get(nse_url)
        else:
            response = nse_session.post(nse_url, json=payload)
        response.raise_for_status()
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
    all_indices_api_url = "https://www.nseindia.com/api/allIndices"
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

    market_watch_index_api_url = f"https://www.nseindia.com/api/NextApi/apiClient/marketWatchApi?functionName=getIndicesData&symbol={selected_index}"
    indices_return_api_url = f"https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getIndicesReturn&&index={selected_index}"
    indices_heatmap_api_url = f"https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getIndicesHeatMap&&index={selected_index}"
    constituents_api_url = f"https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getConstituents&&index={selected_index}&&noofrecords=0"

    market_watch_index_data = nse_fetch_data(market_watch_index_api_url)
    market_watch_index_df = pd.DataFrame(market_watch_index_data.get("data", {}).get("data", []))  #marketStatus, #aduCount

    indices_heatmap_data = nse_fetch_data(indices_heatmap_api_url)
    indices_heatmap_df = pd.DataFrame(indices_heatmap_data.get("data", []))

    constituents_data = nse_fetch_data(constituents_api_url)
    constituents_df = pd.DataFrame(constituents_data.get("data", []))

    if not market_watch_index_df.empty:
        market_watch_index_df['Volume'] = round(market_watch_index_df['totalTradedVolume'].astype(float) / 100000, 2)  #in lakhs
        market_watch_index_df['TradedValue'] = round(market_watch_index_df['totalTradedValue'].astype(float) / 10000000, 2)  #in crores
        market_watch_index_df['Floating_MCap'] = round(market_watch_index_df['ffmc'].astype(float) / 10000000, 2)  #in crores

    final_df = pd.merge(market_watch_index_df, indices_heatmap_df[['symbol', 'VWAP']], how='left', left_on='symbol', right_on='symbol') \
                .merge(constituents_df[['cmSymbol', 'weightage']], how='left', left_on='symbol', right_on='cmSymbol' )

    return final_df.loc[final_df['priority'] == 0, ['companyName', 'symbol', 'weightage','series', 'open', 'dayHigh', 'dayLow', 'lastPrice', 'change', 'pChange', 'VWAP', 'previousClose', 
                                         'Volume', 'TradedValue', 'Floating_MCap', 'yearHigh', 'yearLow', 'perChange30d', 'perChange365d']]


async def fetch_screener_data(url: str) -> pd.DataFrame:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    connector = aiohttp.TCPConnector(ssl=False)
    
    all_pages_data = []
    page = 1
    previous_df = None  # Track the previous page's data
    
    async with aiohttp.ClientSession(connector=connector) as session:
        while True:
            params = {"page": page}
            
            async with session.get(url, headers=headers, params=params) as response:
                if response.status != 200:
                    break
                
                html_content = await response.text()
                
                try:
                    df_list = pd.read_html(StringIO(html_content))
                    target_df = df_list[0].dropna(axis=1, how='all')
                    
                    if target_df.empty:
                        break
                    
                    # SAFEGUARD 1: Check if Screener is just repeating the last page
                    if previous_df is not None and target_df.equals(previous_df):
                        break
                        
                    previous_df = target_df.copy() # Store current df for the next loop
                    
                    all_pages_data.append(target_df)
                    page += 1
                    
                    await asyncio.sleep(0.5)
                    
                except ValueError:
                    break

    if not all_pages_data:
        return pd.DataFrame()
        
    master_df = pd.concat(all_pages_data, ignore_index=True)
    
    if 'S.No.' in master_df.columns:
        master_df = master_df[master_df['S.No.'] != 'S.No.']
    
    # SAFEGUARD 2: Final deduplication based on Company Name
    if 'Name' in master_df.columns:
        master_df = master_df.drop_duplicates(subset=['Name'], keep='first')
    else:
        # Fallback if 'Name' column doesn't exist for some reason
        master_df = master_df.drop_duplicates()

    master_df = master_df.reset_index(drop=True)
    return master_df

@st.cache_data(ttl=3600, show_spinner="Fetching latest market data...")
def help_fetch_screener_data(url: str) -> pd.DataFrame:
    """
    Fetch data from Screener.com for a given URL.

    :param url: The URL of the Screener.com page to fetch data from
    :type url: str

    :return: DataFrame containing the fetched data
    :rtype: pd.DataFrame
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    df = loop.run_until_complete(fetch_screener_data(url))
    loop.close()

    df.drop(columns=['S.No.'], inplace=True, errors='ignore')
    df = df.reset_index(drop=True)
    return df


async def fetch_bse_data(url: str) -> dict:
    headers = {
        "authority": "api.bseindia.com",
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "origin": "https://www.bseindia.com",
        "referer": "https://www.bseindia.com/",
        "accept-language": "en-US,en;q=0.9"
    }
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                json_data = await response.json()
                return json_data
            else:
                print(f"API Error [{response.status}]: {await response.text()}")
                return {}


@st.cache_data(ttl=3600, show_spinner="Fetching latest market data...")
def help_fetch_bse_data(url: str) -> pd.DataFrame:
    if url:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        data = loop.run_until_complete(fetch_bse_data(url))
        loop.close()
    else:
        data = {}
    return data


@st.cache_data(ttl=3600)
def fetch_company_info(category: str, scripcode: str):
    endpoints = {"Company Market Data": f"",
                 "Financials (Income Statement)": f"https://api.bseindia.com/BseIndiaAPI/api/SlbReportNewbeta/w?scripcode={scripcode}",
                 "Annual Report": f"https://api.bseindia.com/BseIndiaAPI/api/AnnualReport_New/w?scripcode={scripcode}",
                 "Corporate Actions": f""}
    out = help_fetch_bse_data(endpoints.get(category))
    if category == "Financials (Income Statement)" and out:
        qtr_full_table_html = f"<table>{out.get('QtlyinCr')}</table>"
        qtr_df_list = pd.read_html(StringIO(qtr_full_table_html))
        qtr_financial_df = qtr_df_list[0].loc[~qtr_df_list[0]['(in Cr.)'].isna() &
                                        (qtr_df_list[0]['(in Cr.)'] != 'Income Statement')]
        yr_full_table_html = f"<table>{out.get('AnninCr')}</table>"
        yr_df_list = pd.read_html(StringIO(yr_full_table_html))
        yrfinancial_df = yr_df_list[0].loc[~yr_df_list[0]['(in Cr.)'].isna() &
                                    (yr_df_list[0]['(in Cr.)'] != 'Income Statement')]
        return qtr_financial_df, yrfinancial_df
    elif category == "Annual Report":
        ar_df = pd.DataFrame(out.get('Table'))
        ar_df = ar_df.loc[:, ["Scripcode", "scrip_name", "Year", "Fld_AuthoriseDate", "PDFDownload"]].head(10)
        return ar_df
    return out


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

# https://www.nseindia.com/market-data/oi-spurts



# sensex:
# ui: https://beta.bseindia.com/stock-share-price/tata-consultancy-services-ltd/tcs/532540/
# https://api.bseindia.com/RealTimeBseIndiaAPI/api/GetSensexData/w