import streamlit as st
import requests
import pandas as pd
import datetime
import time
import json
import asyncio
import aiohttp
from openchart import NSEData
from concurrent.futures import ThreadPoolExecutor


base_nse_url = "https://www.nseindia.com/"
nse_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def mk_etf_strategies_details():
    etf_strategies_details = [{"name": "ETF Ki Dukan", 
                           "conditions": "Volume should be greater than 10000; Remove all Bond/Liquid ETF."}]


# common nse api fetch functionality
def nse_fetch_data(nse_url: str) -> dict:
    """
    Fetch data from NSE API.

    :param nse_url: URL for the NSE API endpoint
    :type nse_url: str

    :return: JSON response from the NSE API
    :rtype: dict
    """
    nse_session = requests.Session()
    nse_session.headers.update(nse_headers)
    nse_session.get(base_nse_url, headers=nse_headers,  timeout=10)
    nse_session.get(base_nse_url+"/option-chain", headers=nse_headers,  timeout=10)

    full_nse_api_url = base_nse_url + nse_url
    # print(f"calling {full_nse_api_url} ..")
    response = nse_session.get(full_nse_api_url)
    output = response.json()
    return output


# get all nse etfs except bonds and less volume of 10k
def get_nse_etfs():
    etf_data_url = "api/etf"
    etf_data = nse_fetch_data(nse_url=etf_data_url)
    etf_data_df = pd.DataFrame(etf_data.get('data'))

    # 'symbol', 'assets', 'open', 'high', 'low', 'ltP', 'chn', 'per', 'qty', 'trdVal', 'nav', 'wkhi', 'wklo', 'prevClose', 
    # 'stockIndClosePrice', 'perChange365d', 'perChange30d', 'date365dAgo', 'date30dAgo', 'ypc',
    # 'mpc', 'xdt', 'cact', 'nearWKH', 'nearWKL', 'chartTodayPath', 'chart30dPath', 'chart365dPath', 'series', 'meta'

    # remove unnecessary columns
    etf_data_df = etf_data_df.loc[:, ['symbol', 'assets', 'open', 'high', 'low', 'ltP', 'prevClose', 'chn', 'per', 'qty', 'nav']]

    # filter the etfs by, volumn > 10000
    etf_data_df['qty'] = etf_data_df['qty'].astype(float)
    etf_data_df = etf_data_df.loc[etf_data_df['qty'] >= 10000]
        
    # filter out bond etfs
    search_values_for_debt_etf = ['LIQUID', 'BOND', 'G-SEC', 'GSEC', 'GILT']
    pattern = '|'.join(search_values_for_debt_etf)
    etf_data_df = etf_data_df[~etf_data_df['assets'].str.contains(pattern, case=False, na=False)]

    # column datatype change & rename the columns
    cols_to_fix_datatype = ['open', 'high', 'low', 'ltP', 'prevClose', 'chn', 'per', 'qty', 'nav']
    etf_data_df[cols_to_fix_datatype] = etf_data_df[cols_to_fix_datatype].apply(pd.to_numeric, errors='coerce')  # 'coerce' turns errors into NaN instead of crashing
    etf_data_df.rename(columns={"symbol": "Symbol", "assets": "Assets", "open": "Open", "high": "High", "low": "Low",
                                "ltP": "Close", "prevClose": "Prev Close", "chn": "Chng", "per": "%Chng", "qty": "Volume", "nav": "iNAV"},
                                inplace=True)
    return etf_data_df.reset_index(drop=True)


# # get 20DMA, 52Wk High & Low data (*not date) from last 31 days daily candle data 
# async def _get_nse_historical_trade_data(symbols, from_date, to_date):
#     # https://www.nseindia.com/api/NextApi/apiClient/GetQuoteApi?functionName=getHistoricalTradeData&symbol=SILVERIETF&series=EQ&fromDate=07-01-2026&toDate=07-02-2026
#     nse_historical_trade_data_url = 'api/NextApi/apiClient/GetQuoteApi?functionName=getHistoricalTradeData&symbol={}&series=EQ&fromDate={}&toDate={}'
#     results = []
#     tasks = []
#     async with aiohttp.ClientSession() as nse_session:
#         for symbol in symbols:
#             full_nse_url = base_nse_url + nse_historical_trade_data_url.format(symbol, from_date, to_date)
#             # print(f"NSE Api: {full_nse_url} has been called ..")
#             tasks.append(nse_session.get(full_nse_url, headers=nse_headers, ssl=False))
#         responses = await asyncio.gather(*tasks)
#         for response in responses:
#             results.append(await response.json())
#     df_list = []
#     for i, res in enumerate(results):
#         out_json = res
#         out_df = pd.DataFrame(out_json)
#         out_df['mtimestamp'] = pd.to_datetime(out_df['mtimestamp'], format='%d-%b-%Y')  # format='%Y-%m-%d'
#         out_df['mtimestamp'] = out_df['mtimestamp'].apply(lambda x: x.date())
#         out_df = out_df.sort_values('mtimestamp', ascending=True)
#         out_df['20DMA'] = out_df['chLastTradedPrice'].rolling(window=20).mean()
#         out_df['63DMA'] = out_df['chLastTradedPrice'].rolling(window=63).mean()
#         df_list.append(out_df.tail(1))
#     df = pd.concat(df_list, ignore_index=True) 

#     # 'chSymbol', 'chSeries', 'chPreviousClsPrice', 'chOpeningPrice','chTradeHighPrice', 'chTradeLowPrice', 'chLastTradedPrice','chClosingPrice', 'vwap', 'chTotTradedQty', 'chTotTradedVal','chTotalTrades', 'ch52WeekHighPrice', 'ch52WeekLowPrice', 'mtimestamp'
#     df = df.loc[:, ['mtimestamp', 'chSymbol', 'chPreviousClsPrice', 'chOpeningPrice', 'chTradeHighPrice', 'chTradeLowPrice', 'chLastTradedPrice', 'vwap', 
#                     '20DMA', '63DMA', 'chTotTradedQty', 'chTotalTrades', 'ch52WeekHighPrice', 'ch52WeekLowPrice']]
#     df.rename(columns={'mtimestamp': 'Date', 'chSymbol': 'Symbol', 'chPreviousClsPrice': 'Prev Close', 'chOpeningPrice': 'Open', 'chTradeHighPrice': 'High', 
#                        'chTradeLowPrice': 'Low', 'chLastTradedPrice': 'Close', 'vwap': 'VWAP', 'chTotTradedQty': 'Volume', 
#                        'chTotalTrades': 'Total Trades', 'ch52WeekHighPrice': '52wk High', 'ch52WeekLowPrice': '52wk Low'},
#                        inplace=True)
#     return df


# # get all time high low data and date
# async def _get_nse_alltime_high_low(symbols):
#     nse_alltime_high_low_url = 'api/NextApi/apiClient/GetQuoteApi?functionName=getHistoricalPeriodic52WeekHighLow&symbol={}'
#     results = []
#     tasks = []
#     async with aiohttp.ClientSession() as nse_session:
#         for symbol in symbols:
#             full_nse_url = base_nse_url + nse_alltime_high_low_url.format(symbol)
#             # print(f"NSE Api: {full_nse_url} has been called ..")
#             tasks.append(nse_session.get(full_nse_url, headers=nse_headers, ssl=False))
#         responses = await asyncio.gather(*tasks)
#         for response in responses:
#             results.append(await response.json())
#     df_list = []
#     for i, res in enumerate(results):
#         out_json = res.get('data')
#         out_df = pd.DataFrame(out_json, index=[0])
#         out_df['Symbol'] = symbols[i]
#         out_df['maxDate'] = pd.to_datetime(out_df['maxDate'], format='%d-%b-%Y') 
#         out_df['minDate'] = pd.to_datetime(out_df['minDate'], format='%d-%b-%Y') 
#         df_list.append(out_df)
#     df = pd.concat(df_list, ignore_index=True)
#     df.rename(columns={'max': 'ATH', 'maxDate': 'ATH Dt', 'min': 'ATL', 'minDate': 'ATL Dt'}, inplace=True)
#     return df.loc[:, ['Symbol', 'ATH', 'ATH Dt', 'ATL', 'ATL Dt']]


async def _get_nse_52wk_high_low(symbols):
    # api/NextApi/apiClient/GetQuoteApi?functionName=getHistoricalPeriodicData&symbol={symbol}&type=weekly52
    # api/NextApi/apiClient/GetQuoteApi?functionName=getHistoricalPeriodicData&symbol={symbol}&year=2026&type=yearly
    # api/NextApi/apiClient/GetQuoteApi?functionName=getHistoricalPeriodicData&symbol={symbol}&year=2026&month=02&type=monthly
    nse_52wk_high_low_url = 'api/NextApi/apiClient/GetQuoteApi?functionName=getHistoricalPeriodicData&symbol={}&type=weekly52'
    results = []
    tasks = []
    async with aiohttp.ClientSession() as nse_session:
        for symbol in symbols:
            full_nse_url = base_nse_url + nse_52wk_high_low_url.format(symbol)
            # print(f"NSE Api: {full_nse_url} has been called ..")
            tasks.append(nse_session.get(full_nse_url, headers=nse_headers, ssl=False))
        responses = await asyncio.gather(*tasks)
        for response in responses:
            results.append(await response.json())
    df_list = []
    for i, res in enumerate(results):
        data = dict()
        data['Symbol'] = symbols[i]
        data['52Wk High'] = float(res.get('high').get('high_price'))
        data['52Wk High Dt'] = res.get('high').get('high_price_date')
        data['52Wk Low'] = float(res.get('low').get('low_price'))
        data['52Wk Low Dt'] = res.get('low').get('low_price_date')
        out_df = pd.DataFrame(data, index=[0])
        out_df['52Wk High Dt'] = pd.to_datetime(out_df['52Wk High Dt'], format='%d-%b-%Y')
        out_df['52Wk High Dt'] = out_df['52Wk High Dt'].apply(lambda x: x.date())
        out_df['52Wk Low Dt'] = pd.to_datetime(out_df['52Wk Low Dt'], format='%d-%b-%Y')
        out_df['52Wk Low Dt'] = out_df['52Wk Low Dt'].apply(lambda x: x.date())
        df_list.append(out_df)
    df = pd.concat(df_list, ignore_index=True)
    return df.loc[:, ['Symbol', '52Wk High', '52Wk High Dt', '52Wk Low', '52Wk Low Dt']]


def _openchart_fetch_nse_history(symbol):
    nse = NSEData()
    try:
        end = datetime.datetime.now()
        start = end - datetime.timedelta(days=160)
        df = nse.historical(symbol, 'EQ', start, end, '1d')
        if df is not None and not df.empty:
            df['Date'] = pd.to_datetime(df.index).date
            # df['Date'] = df['Date'].apply(lambda x: x.date())
            df = df.sort_values('Date', ascending=True)

            df['PrevClose'] = df['Close'].shift(1)

            # df['%Chng'] = df['Close'].pct_change() * 100
            # df['%Chng'] = df['%Chng'].round(2)
            df['%Chng'] = ((df['Close'] - df['PrevClose']) / df['PrevClose']) * 100
            df['%Chng'] = df['%Chng'].round(2)

            df['20DMA'] = df['Close'].rolling(window=20).mean()
            df['100DMA'] = df['Close'].rolling(window=100).mean()
            df['Symbol'] = symbol.split("-EQ")[0]
            
            return df.loc[:, ["Symbol", "Open", "High", "Low", "Close", "PrevClose", "%Chng", "Volume", "20DMA", "100DMA", "Date"]].tail(1)
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
    return None


@st.cache_data(ttl=3600, show_spinner="Fetching NSE ETF Trade Symbols...")
def streamlit_nse_etf_trade_data():
    etf_data_df = get_nse_etfs()
    # etf_symbols = etf_data_df['Symbol'].unique().tolist()
    return etf_data_df


@st.cache_data(ttl=3600, show_spinner="Fetching NSE ETF Historical Data from OpenChart...")
def streamlit_nse_etf_historical_openchart(nse_etf_symbols):
    unique_symbols_eq = [x+'-EQ' for x in nse_etf_symbols]
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(_openchart_fetch_nse_history, unique_symbols_eq))
    valid_dfs = [d for d in results if d is not None]
    if valid_dfs:
        final_df = pd.concat(valid_dfs, ignore_index=True)
    else:
        final_df = pd.DataFrame()
    return final_df


# @st.cache_data(ttl=3600, show_spinner="Fetching NSE ETF Historical Data...")
# def streamlit_nse_etf_historical_data(etf_symbols):
#     cur_date_obj = datetime.datetime.today()
#     from_date_obj = cur_date_obj - datetime.timedelta(days=90)
#     from_date = from_date_obj.strftime("%d-%m-%Y")
#     to_date = cur_date_obj.strftime("%d-%m-%Y")

#     nse_etf_hist_trade_df = asyncio.run(_get_nse_historical_trade_data(etf_symbols, from_date, to_date))
#     # nse_etf_hist_trade_df = nse_etf_hist_trade_df.loc[:,['Date', 'Symbol', 'Prev Close', 'Open', 'High', 'Low', 'Close', 'VWAP', '20DMA', 'Total Trades', '52wk High', '52wk Low']]
#     nse_etf_hist_trade_df = nse_etf_hist_trade_df.loc[:,['Date', 'Symbol', 'VWAP', '20DMA', '63DMA', 'Total Trades', '52wk High', '52wk Low']]
#     # time.sleep(2)
#     # # All time High Low data with date
#     # nse_etf_alltime_high_low_df = asyncio.run(_get_nse_alltime_high_low(unique_symbols))
#     return nse_etf_hist_trade_df


@st.cache_data(ttl=3600, show_spinner="Fetching NSE ETF 52Wk High Low Data...")
def streamlit_nse_etf_52wk_high_low(nse_etf_symbols):
    nse_etf_52wk_high_low_df = asyncio.run(_get_nse_52wk_high_low(nse_etf_symbols))
    return nse_etf_52wk_high_low_df