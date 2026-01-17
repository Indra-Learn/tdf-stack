import streamlit as st
import pandas as pd
from datetime import datetime as dt, timedelta as td
from time import sleep
from functools import partial
import concurrent.futures
# import logging

# # uncomment below block if run from local
# import os, sys
# absolute_parent = os.path.abspath(os.path.join(os.getcwd()))
# sys.path.append(absolute_parent)

from tdf_utility.trading.nse_api import NSE_API, get_nse_india_vix, get_nse_market_status_daily, get_nifty_heatmap
from tdf_utility.trading.ep_api import fetch_fii_dii_data

# logging.basicConfig(level=logging.INFO)

def _load_graph_data_to_df(object: dict):
    identifier = object.get('data').get('identifier')
    # name = objecct.get('data').get('name')
    grapth_data = object.get('data').get('grapthData')
    df = pd.DataFrame(grapth_data, columns=['Timestamp', 'Price', 'Code'])
    df['Date'] = pd.to_datetime(df['Timestamp'], unit='ms')
    return df, identifier

# ttl=3000 means "Refresh this data every 50 minutes (50*60 seconds)"
@st.cache_data(ttl=3000, show_spinner="Fetching Market Data...")
def sourcing_viz_data():
    duration = "1Y"
    current_date = dt.today()
    year = str(current_date.year)
    from_dt = (current_date - td(days=365)).strftime("%d-%m-%Y")
    to_dt = (current_date).strftime("%d-%m-%Y")

    nse_api = NSE_API()
    
    nifty_50_historical_data = nse_api._get_data(f"api/NextApi/apiClient/historicalGraph?functionName=getIndexChart&&index=NIFTY%2050&flag={duration}")

    india_vix_historical_data = get_nse_india_vix()
    india_vix_historical_data['date'] = pd.to_datetime(india_vix_historical_data['date'], format='%d-%b-%Y')

    sleep(2)
    gold_historical_data = nse_api._get_data(f"api/historical-spot-price?symbol=GOLD&fromDate={from_dt}&toDate={to_dt}")
    gold_historical_df = pd.DataFrame(gold_historical_data['data']) \
                                        .loc[:, ['UpdatedDate', 'SpotPrice2']] \
                                        .rename(columns={'UpdatedDate': 'Date', 'SpotPrice2': 'Gold 10gm'})
    gold_historical_df['Date'] = pd.to_datetime(gold_historical_df['Date'], format='%d-%b-%Y')
    gold_historical_df['Gold 10gm'] = gold_historical_df['Gold 10gm'].astype(float)

    sleep(2)
    silver_historical_data = nse_api._get_data(f"api/historical-spot-price?symbol=SILVER&fromDate={from_dt}&toDate={to_dt}")
    silver_historical_df = pd.DataFrame(silver_historical_data['data']) \
                                        .loc[:, ['UpdatedDate', 'SpotPrice2']] \
                                        .rename(columns={'UpdatedDate': 'Date', 'SpotPrice2': 'Silver 1kg'})
    silver_historical_df['Date'] = pd.to_datetime(silver_historical_df['Date'], format='%d-%b-%Y')
    silver_historical_df['Silver 1kg'] = silver_historical_df['Silver 1kg'].astype(float)

    crudeoil_historical_data = nse_api._get_data(f"api/historical-spot-price?symbol=CRUDEOIL&fromDate={from_dt}&toDate={to_dt}")
    crudeoil_historical_df = pd.DataFrame(crudeoil_historical_data['data']) \
                                        .loc[:, ['UpdatedDate', 'SpotPrice1']] \
                                        .rename(columns={'UpdatedDate': 'Date', 'SpotPrice1': 'Crude Oil'})
    crudeoil_historical_df['Date'] = pd.to_datetime(crudeoil_historical_df['Date'], format='%d-%b-%Y')
    crudeoil_historical_df['Crude Oil'] = crudeoil_historical_df['Crude Oil'].astype(float)

    fii_dii_data_df = fetch_fii_dii_data()

    nifty50_historical_graph_df, nifty50_graph_identifier = _load_graph_data_to_df(nifty_50_historical_data)

    viz_df = pd.merge(nifty50_historical_graph_df.loc[:, ['Date', 'Price']].rename(columns={'Price': 'Nifty 50'}),
                india_vix_historical_data[['date', 'close']].rename(columns={'date': 'Date', 'close': 'India VIX'}),
                on='Date', how='left')
    viz_df = pd.merge(viz_df, gold_historical_df, on='Date', how='left')
    viz_df = pd.merge(viz_df, silver_historical_df, on='Date', how='left')
    viz_df = pd.merge(viz_df, crudeoil_historical_df, on='Date', how='left')
    viz_df = pd.merge(viz_df, fii_dii_data_df, on='Date', how='left')

    # market_status = get_nse_market_status_daily()
    # st.sidebar.write("Data is fetched and stored into cache")
    return viz_df


@st.cache_data(ttl=3000, show_spinner="Fetching Market Data...")
def sourcing_nifty_index_data():
    nse_api = NSE_API()
    nifty_heatmap_df = get_nifty_heatmap()
    nifty_heatmap_df["Company Profile"] = nifty_heatmap_df["symbol"].apply(lambda x: f"/company_profile?ticker_symbol={x}")
    # st.sidebar.write("Data is fetched and stored into cache")
    return nifty_heatmap_df


@st.cache_data(ttl=3000, show_spinner="Fetching Market Data...")
def company_viz_df(company_ticker, from_dt:str=None, to_dt:str=None):
    company_details = "https://www.nseindia.com/api/NextApi/apiClient/GetQuoteApi?functionName=getSymbolData&marketType=N&series=EQ&symbol=BHARTIARTL"

    company_1y_chart_data = "https://www.nseindia.com/api/NextApi/apiClient/GetQuoteApi?functionName=getSymbolChartData&symbol=BHARTIARTLEQN&days=1Y"
    
    
    nse_api = NSE_API()
    df_list = list()

    company_name_url = f"api/NextApi/apiClient/GetQuoteApi?functionName=getSymbolName&symbol={company_ticker}"
    company_name = nse_api._get_data(company_name_url).get("companyName")

    company_yearwise_url = f"api/NextApi/apiClient/GetQuoteApi?functionName=getYearwiseData&symbol={company_ticker}QN"
    # company_yearwise_data = 
    

    if from_dt and to_dt:
        to_dt = dt.strptime(to_dt, '%d-%m-%Y')
        from_dt = dt.strptime(from_dt, '%d-%m-%Y')
        company_corp_action_url = f"api/NextApi/apiClient/GetQuoteApi?functionName=getCorpAction&symbol={company_ticker}&type=W&marketApiType=equities&ex_from_date={from_dt}&ex_to_date={to_dt}"
    else:
        to_dt = dt.now()
        from_dt = to_dt - td(days=365)
        company_corp_action_url = f"api/NextApi/apiClient/GetQuoteApi?functionName=getCorpAction&symbol={company_ticker}&type=W&marketApiType=equities&ex_from_date={from_dt.strftime("%d-%m-%Y")}&ex_to_date={to_dt.strftime("%d-%m-%Y")}"

    while from_dt < to_dt:
        from_dt_30 =  (to_dt - td(days=30))
        company_historical_tradedata_url = f'api/NextApi/apiClient/GetQuoteApi?functionName=getHistoricalTradeData&symbol={company_ticker}&series=EQ&fromDate={from_dt_30.strftime("%d-%m-%Y")}&toDate={to_dt.strftime("%d-%m-%Y")}'
        company_trade_data = nse_api._get_data(company_historical_tradedata_url)
        df_list.append(pd.DataFrame(company_trade_data))
        to_dt = (from_dt_30 - td(days=1))
        
    company_trade_data_df = pd.concat(df_list[::-1], ignore_index=True)
    company_trade_data_df["Date"] = pd.to_datetime(company_trade_data_df.get("mtimestamp"), format='%d-%b-%Y')
    company_trade_data_df.rename(columns={"chSymbol": "Symbol", 
                                          "chOpeningPrice": "Open",
                                          "chTradeHighPrice": "High",
                                          "chTradeLowPrice": "Low",
                                          "chClosingPrice": "Close",
                                          "chPreviousClsPrice": "Prev Close",
                                          "chLastTradedPrice": "LTP",
                                          "vwap": "VWAP",
                                          "chTotTradedQty": "Volume",	
                                          "chTotTradedVal": "Turnover",	
                                          "chTotalTrades": "Transactions",
                                          "ch52WeekHighPrice": "52 Week High",
                                          "ch52WeekLowPrice": "52 Week Low"}, inplace=True)
    company_trade_data_df = company_trade_data_df.loc[:, ["Date", "Symbol", "Open", "High", "Low", "Close", "Prev Close", "LTP", "VWAP", "Volume", "Turnover", "Transactions", "52 Week High", "52 Week Low"]]
    company_trade_data_df = company_trade_data_df.sort_values(by='Date')
    company_trade_data_df.reset_index(drop=True, inplace=True)
    company_trade_data_df['7_DMA'] = company_trade_data_df['Close'].rolling(window=7).mean()
    company_trade_data_df['21_DMA'] = company_trade_data_df['Close'].rolling(window=21).mean()
    
    # company_df = pd.DataFrame(nse_api._get_data(company_url))
    company_corp_action_df = pd.DataFrame(nse_api._get_data(company_corp_action_url))
    return company_name, company_trade_data_df, company_corp_action_df


def company_df(symbol):
    nse_api = NSE_API()
    df_list = list()
    to_dt = dt.now()
    from_dt = to_dt - td(days=90)
    
    if "&" in symbol:
        safe_symbol = symbol.replace("&", "%26")
    else:
        safe_symbol = symbol

    # company_name_url = f"api/NextApi/apiClient/GetQuoteApi?functionName=getSymbolName&symbol={symbol}"
    # company_name = nse_api._get_data(company_name_url).get("companyName")
    while from_dt < to_dt:
        from_dt_90 =  (to_dt - td(days=30))
        company_historical_tradedata_url = f'api/NextApi/apiClient/GetQuoteApi?functionName=getHistoricalTradeData&symbol={safe_symbol}&series=EQ&fromDate={from_dt_90.strftime("%d-%m-%Y")}&toDate={to_dt.strftime("%d-%m-%Y")}'
        company_trade_data = nse_api._get_data(company_historical_tradedata_url)
        df_list.append(pd.DataFrame(company_trade_data))
        to_dt = (from_dt_90 - td(days=1))
    company_trade_data_df = pd.concat(df_list[::-1], ignore_index=True)
    company_trade_data_df["Date"] = pd.to_datetime(company_trade_data_df.get("mtimestamp"), format='%d-%b-%Y')
    company_trade_data_df.rename(columns={'chSymbol': 'Symbol', 'chSeries': 'Series', 'chPreviousClsPrice': 'Prev Close', 
        'chOpeningPrice': 'Open', 'chTradeHighPrice': 'High', 'chTradeLowPrice': 'Low', 'chLastTradedPrice': 'LTP',
       'chClosingPrice': 'Close', 'vwap': 'VWAP', 'chTotTradedQty': 'Volumn', 'chTotTradedVal': 'Traded Value',
       'chTotalTrades': 'Transactions', 'ch52WeekHighPrice': '52Week High', 'ch52WeekLowPrice': '52Week Low'}, inplace=True)
    company_trade_data_df = company_trade_data_df.sort_values(by='Date', ascending=False)
    company_trade_data_df.reset_index(drop=True, inplace=True)

    # Price Information
    company_price_info_url = f"api/NextApi/apiClient/GetQuoteApi?functionName=getSymbolData&marketType=N&series=EQ&symbol={safe_symbol}"
    
    company_price_info_data = nse_api._get_data(company_price_info_url).get("equityResponse")[0].get("priceInfo")
    company_trade_data_df["52Week High Date"] = company_price_info_data.get("yearHightDt")
    company_trade_data_df["52Week Low Date"] = company_price_info_data.get("yearLowDt")

    company_trade_data_df["52Week High Date"] = pd.to_datetime(company_trade_data_df.get("52Week High Date"), format='%d-%b-%Y %H:%M:%S').dt.date
    company_trade_data_df["52Week Low Date"] = pd.to_datetime(company_trade_data_df.get("52Week Low Date"), format='%d-%b-%Y %H:%M:%S').dt.date
    
    return company_trade_data_df


@st.cache_data(ttl=3000, show_spinner="Fetching Market Data...")
def get_nifty_index_data(nifty_index_symbol):
    nse_api = NSE_API()

    # Market Turnover
    # market_time = nse_api._get_data("api/NextApi/dynamicApi?functionName=getCurrentTime")

    # Index Data
    nifty_index_url = f"api/equity-stockIndices?index={nifty_index_symbol}"
    nifty_index_data = nse_api._get_data(nifty_index_url)

    nifty_date = dt.strptime(nifty_index_data.get("timestamp"), "%d-%b-%Y %H:%M:%S").date()

    nifty_index_stocks_df = pd.DataFrame(nifty_index_data.get("data"))
    nifty_index_stocks_df = nifty_index_stocks_df.loc[(nifty_index_stocks_df["priority"] != 1), ["symbol", "open", "dayHigh", "dayLow", "lastPrice",
                            "previousClose", "change", "pChange", "yearHigh", "yearLow", "totalTradedVolume", "totalTradedValue", 
                            "nearWKH", "nearWKL", "perChange365d", "perChange30d"]]
    nifty_index_stocks_df.rename(columns={"symbol": "Symbol", "open": "Open", "dayHigh": "High", "dayLow": "Low", "lastPrice": "Close",
                            "previousClose": "Prev Close", "change": "Change", "pChange": "P Change", "yearHigh": "52Week High", 
                            "yearLow": "52Week Low", "totalTradedVolume": "Volume", "totalTradedValue": "Traded Value"}, 
                            inplace=True)
    
    # bins = [0, 50, 100, 250, 500]
    # labels = ['Nifty 50', 'Nifty Next50', 'Nifty Midcap 150', 'Others']
    # nifty_index_stocks_df['Nifty Index'] = pd.cut(nifty_index_stocks_df.index, bins=bins, labels=labels, right=False)
    nifty_index_stocks_df['Nifty Index'] = nifty_index_symbol
    nifty_index_stocks_list = nifty_index_stocks_df['Symbol'].unique().tolist()
    
    stock_df = pd.DataFrame()
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        stock_df_list = list(executor.map(company_df, nifty_index_stocks_list))
    stock_df = pd.concat(stock_df_list)
    stock_df["Date"] = stock_df["Date"].dt.date
    # stock_df["52Week High Date"] = stock_df["52Week High Date"].dt.date
    # stock_df["52Week Low Date"] = stock_df["52Week Low Date"].dt.date
    stock_df = stock_df.loc[:,['Symbol', 'Date', 'Prev Close', 'Open', 'High', 'Low', 'LTP', 'Close', 'VWAP', 'Volumn', 'Traded Value', 'Transactions', '52Week High', '52Week High Date', '52Week Low', '52Week Low Date']]
    return nifty_date, nifty_index_stocks_df, stock_df