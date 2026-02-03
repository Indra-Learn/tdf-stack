import streamlit as st
import aiohttp
import asyncio
import json
import time
import pandas as pd
# import logging

# logging.basicConfig(level = logging.INFO, filename = 'tdf_streamlit_log.log')


base_nse_url = "https://www.nseindia.com/"
nse_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
nifty_500_index_list = ["NIFTY 50", "NIFTY NEXT 50", "NIFTY MIDCAP 150", "NIFTY SMLCAP 250"]


def get_tasks(session, nifty_api_url, index_list):
    tasks = []
    if type(index_list) is list:
        for index_name in index_list:
            nse_url = base_nse_url + nifty_api_url.format(index_name)
            # print(f"calling {nse_url} ..")
            tasks.append(session.get(nse_url, headers=nse_headers, ssl=False))
    elif type(index_list) is pd.DataFrame:
        for index_name in index_list['safe_symbol'].tolist():
            # if index_name == "PRAJIND":
            #     continue
            nse_url = base_nse_url + nifty_api_url.format(index_name)
            # print(f"calling {nse_url} ..")
            tasks.append(session.get(nse_url, headers=nse_headers, ssl=False))
    return tasks


async def get_nifty_index_sector():
    # nifty_sector_url = "api/heatmap-index?type={}"  # "Sectoral Indices"
    nifty_sector_url = "api/{}"
    results = []
    async with aiohttp.ClientSession() as nse_session:
        tasks = get_tasks(nse_session, nifty_sector_url, ["allIndices"])
        responses = await asyncio.gather(*tasks)
        for response in responses:
            results.append(await response.json())
    df_list = []
    for i, res in enumerate(results):
        out_json = res.get('data')
        out_df = pd.DataFrame(out_json)
        df_list.append(out_df)
    results_df = pd.concat(df_list, ignore_index=True)
    # indexSymbol, variation ,'chart365dPath','chart30dPath','chartTodayPath' ,'indicativeClose'
    results_df = results_df.loc[:, ['key','index','last','percentChange','open','high','low','previousClose',
                                    'yearHigh','yearLow','pe','pb','dy','declines','advances','unchanged',
                                    'perChange365d','perChange30d','date365dAgo','date30dAgo','previousDay',
                                    'oneWeekAgo','oneMonthAgoVal','oneWeekAgoVal','oneYearAgoVal','previousDayVal']]
    results_df.rename(columns={"index": "Index", "last": "LTP", "percentChange": "%CHNG", "open": "OPEN",
                                "high": "HIGH", "low": "LOW", "previousClose": "PREV CLOSE",
                                "yearHigh": "52W H", "yearLow": "52W L", "perChange365d": "365D %CHNG", 
                                "perChange30d": "30D %CHNG", "date365dAgo": "365D DATE", "date30dAgo": "30D DATE", "previousDay": "PREV DAY",
                                    "oneWeekAgo": "1W AGO", "oneMonthAgoVal": "1M AGO VAL", "oneWeekAgoVal": "1W AGO VAL", 
                                    "oneYearAgoVal": "1Y AGO VAL", "previousDayVal": "PREV DAY VAL"}, inplace=True)
    return results_df


async def get_nifty_index_constituents(nifty_index_list: list):
    nifty_index_constituents_url = 'api/NextApi/apiClient/indexTrackerApi?functionName=getConstituents&&index={}&&noofrecords=0'
    results = []
    async with aiohttp.ClientSession() as nse_session:
        tasks = get_tasks(nse_session, nifty_index_constituents_url, nifty_index_list)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            results.append(await response.json())
    df_list = []
    for i, res in enumerate(results):
        out_json = res.get('data')
        out_df = pd.DataFrame(out_json)
        out_df['Index'] = nifty_index_list[i]
        df_list.append(out_df)
    results_df = pd.concat(df_list, ignore_index=True)
    results_df.rename(columns={"cmSymbol": "Symbol", "weightage": "Weightage(%)", "lasttradedPrice": "LTP", 
                                "change": "CHNG", "pchange": "%CHNG", "totaltradedquantity": "VOLUME (in Lakhs)", 
                                "totaltradedvalue": "VALUE (in Cr)"}, inplace=True)
    return results_df


async def get_nse_stock_price_info(nifty_stocks_df: str):
    nifty_stocks_df['safe_symbol'] = nifty_stocks_df['Symbol'].apply(lambda symbol: symbol.replace("&", "%26"))
    company_price_info_url = "api/NextApi/apiClient/GetQuoteApi?functionName=getSymbolData&marketType=N&series=EQ&symbol={}"
    results = []
    async with aiohttp.ClientSession() as nse_session:
        tasks = get_tasks(nse_session, company_price_info_url, nifty_stocks_df['safe_symbol'].tolist())
        responses = await asyncio.gather(*tasks)
        for response in responses:
            results.append(await response.json())
            # data = await response.text()
            # json_data = json.loads(data)
            # results.append(json_data)
    df_list = []
    for i, res in enumerate(results):
        out_json = res.get("equityResponse")[0].get("priceInfo")
        out_df = pd.DataFrame(out_json, index=["A"])
        out_df['Symbol'] = res.get("equityResponse")[0].get("metaData").get("symbol")
        # out_df['Index'] = res.get("equityResponse")[0].get("secInfo").get("index")
        df_list.append(out_df)
    results_df = pd.concat(df_list, ignore_index=True)
    # results_df = pd.merge(results_df, nifty_stocks_df, left_on='Symbol', right_on='Symbol', how='left')
    return results_df
    

# def sourcing_viz_data():
#     duration = "1Y"
#     current_date = dt.today()
#     year = str(current_date.year)
#     from_dt = (current_date - td(days=365)).strftime("%d-%m-%Y")
#     to_dt = (current_date).strftime("%d-%m-%Y")

#     nse_api = NSE_API()
    
#     nifty_50_historical_data = nse_api._get_data(f"api/NextApi/apiClient/historicalGraph?functionName=getIndexChart&&index=NIFTY%2050&flag={duration}")

#     india_vix_historical_data = get_nse_india_vix()
#     india_vix_historical_data['date'] = pd.to_datetime(india_vix_historical_data['date'], format='%d-%b-%Y')

#     sleep(2)
#     gold_historical_data = nse_api._get_data(f"api/historical-spot-price?symbol=GOLD&fromDate={from_dt}&toDate={to_dt}")
#     gold_historical_df = pd.DataFrame(gold_historical_data['data']) \
#                                         .loc[:, ['UpdatedDate', 'SpotPrice2']] \
#                                         .rename(columns={'UpdatedDate': 'Date', 'SpotPrice2': 'Gold 10gm'})
#     gold_historical_df['Date'] = pd.to_datetime(gold_historical_df['Date'], format='%d-%b-%Y')
#     gold_historical_df['Gold 10gm'] = gold_historical_df['Gold 10gm'].astype(float)

#     sleep(2)
#     silver_historical_data = nse_api._get_data(f"api/historical-spot-price?symbol=SILVER&fromDate={from_dt}&toDate={to_dt}")
#     silver_historical_df = pd.DataFrame(silver_historical_data['data']) \
#                                         .loc[:, ['UpdatedDate', 'SpotPrice2']] \
#                                         .rename(columns={'UpdatedDate': 'Date', 'SpotPrice2': 'Silver 1kg'})
#     silver_historical_df['Date'] = pd.to_datetime(silver_historical_df['Date'], format='%d-%b-%Y')
#     silver_historical_df['Silver 1kg'] = silver_historical_df['Silver 1kg'].astype(float)

#     crudeoil_historical_data = nse_api._get_data(f"api/historical-spot-price?symbol=CRUDEOIL&fromDate={from_dt}&toDate={to_dt}")
#     crudeoil_historical_df = pd.DataFrame(crudeoil_historical_data['data']) \
#                                         .loc[:, ['UpdatedDate', 'SpotPrice1']] \
#                                         .rename(columns={'UpdatedDate': 'Date', 'SpotPrice1': 'Crude Oil'})
#     crudeoil_historical_df['Date'] = pd.to_datetime(crudeoil_historical_df['Date'], format='%d-%b-%Y')
#     crudeoil_historical_df['Crude Oil'] = crudeoil_historical_df['Crude Oil'].astype(float)

#     fii_dii_data_df = fetch_fii_dii_data()

#     nifty50_historical_graph_df, nifty50_graph_identifier = _load_graph_data_to_df(nifty_50_historical_data)

#     viz_df = pd.merge(nifty50_historical_graph_df.loc[:, ['Date', 'Price']].rename(columns={'Price': 'Nifty 50'}),
#                 india_vix_historical_data[['date', 'close']].rename(columns={'date': 'Date', 'close': 'India VIX'}),
#                 on='Date', how='left')
#     viz_df = pd.merge(viz_df, gold_historical_df, on='Date', how='left')
#     viz_df = pd.merge(viz_df, silver_historical_df, on='Date', how='left')
#     viz_df = pd.merge(viz_df, crudeoil_historical_df, on='Date', how='left')
#     viz_df = pd.merge(viz_df, fii_dii_data_df, on='Date', how='left')

#     # market_status = get_nse_market_status_daily()
#     # st.sidebar.write("Data is fetched and stored into cache")
#     return viz_df


@st.cache_data(ttl=3600, show_spinner="Fetching Nifty Index Sector & Constituents Data Asynchronously...")
def streamlit_market_overview(nifty_500_index_list):
    nifty_sector_df = asyncio.run(get_nifty_index_sector())

    nifty_index_constituents_df = asyncio.run(get_nifty_index_constituents(nifty_500_index_list))

    nifty_500_stock_list = nifty_index_constituents_df['Symbol'].unique().tolist()
    nifty_500_index_stocks_df = nifty_index_constituents_df[['Symbol', 'Index']].drop_duplicates(subset=['Symbol'])
    return nifty_sector_df, nifty_index_constituents_df, nifty_500_stock_list, nifty_500_index_stocks_df

@st.cache_data(ttl=3600, show_spinner="Fetching Nifty 500 Stocks Data Asynchronously...")
def streamlit_nifty_stock_screener(nifty_500_index_stocks_df, index_filter):
    filtered_nifty_500_index_stocks_df = nifty_500_index_stocks_df.loc[nifty_500_index_stocks_df['Index'] == index_filter]
    # filtered_nifty_500_index_stocks_df = nifty_500_index_stocks_df.copy()
    nse_stock_price_info_df = asyncio.run(get_nse_stock_price_info(filtered_nifty_500_index_stocks_df))
    nse_stock_price_info_df['Index'] = index_filter
    nse_stock_price_info_df.rename(columns={"yearHightDt": "52W H Dt", "yearLowDt": "52W L Dt", "yearHigh": "52W H", "yearLow": "52W L",
                                            "priceBand": "Price Band"},
                                   inplace=True)
    return nse_stock_price_info_df.loc[:, ["Symbol", "52W H", "52W L", "52W H Dt", "52W L Dt", "Price Band", "Index"]]


if __name__ == "__main__":
    final_result_nifty_index_constituents_df = asyncio.run(get_nifty_index_constituents(nifty_500_index_list))
    # print(final_result_nifty_index_constituents_df)
    # print(final_result_nifty_index_constituents_df.head())
    # print(final_result_nifty_index_constituents_df.columns)
    # print(final_result_nifty_index_constituents_df.shape)

