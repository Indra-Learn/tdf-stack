import pandas as pd
from datetime import datetime as dt, timedelta as td
from time import sleep

from tdf_utility.trading.nse_api import NSE_API, get_nse_india_vix, get_nse_market_status_daily, get_nifty_heatmap
from tdf_utility.trading.ep_api import fetch_fii_dii_data

def _load_graph_data_to_df(object: dict):
    identifier = object.get('data').get('identifier')
    # name = objecct.get('data').get('name')
    grapth_data = object.get('data').get('grapthData')
    df = pd.DataFrame(grapth_data, columns=['Timestamp', 'Price', 'Code'])
    df['Date'] = pd.to_datetime(df['Timestamp'], unit='ms')
    return df, identifier

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
    return viz_df


def sourcing_nifty_index_data():
    nse_api = NSE_API()
    nifty_heatmap_df = get_nifty_heatmap()
    nifty_heatmap_df["Company Profile"] = nifty_heatmap_df["symbol"].apply(lambda x: f"/company_profile?ticker_symbol={x}")
    return nifty_heatmap_df