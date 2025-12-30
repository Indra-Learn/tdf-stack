"""
1. https://www.nseindia.com/api/marketStatus
2. https://www.nseindia.com/api/othermarketStatus?market=CMOT

3. Graph Trade data: https://www.nseindia.com/api/chart-databyindex-dynamic?index=GROWWDEFNCEQN&type=symbol
4. corporate info: https://www.nseindia.com/api/top-corp-info?symbol=GROWWDEFNC&market=equities&series=EQ
5. serv: https://www.nseindia.com/api/regulation/serv?symbol=GROWWDEFNC&series=EQ

6. Market Turnover: https://www.nseindia.com/api/NextApi/apiClient?functionName=getMarketTurnoverSummary

1. All Index data daily: https://www.nseindia.com/api/NextApi/apiClient?functionName=getIndexData&&type=All
1. all indices: https://www.nseindia.com/api/NextApi/apiClient/homeApi?functionName=getIndicesData

2. Gift Nifty: https://www.nseindia.com/api/NextApi/apiClient?functionName=getGiftNifty
3. market turnover: https://www.nseindia.com/api/NextApi/apiClient?functionName=getMarketTurnover
4. market turnover summary: https://www.nseindia.com/api/NextApi/apiClient?functionName=getMarketTurnoverSummary
5. market statistics: https://www.nseindia.com/api/NextApi/apiClient?functionName=getMarketStatistics
6. market few stocks or marque data: https://www.nseindia.com/api/NextApi/apiClient?functionName=getMarqueData
7. get current time: https://www.nseindia.com/api/NextApi/dynamicApi?functionName=getCurrentTime
8. listing data: https://www.nseindia.com/api/NextApi/apiClient?functionName=getListingData$0
9. 

https://www.nseindia.com/api/NextApi/apiClient?functionName=getGiftNifty

https://www.nseindia.com/api/NextApi/apiClient?functionName=getIndexData&&type=All

https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getAdvanceDecline&&index=NIFTY%2050

 https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getIndexData&&index=NIFTY%2050

https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getIndicesReturn&&index=NIFTY%2050

https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getIndexChart&&index=NIFTY%2050&flag=1D
https://www.nseindia.com/api/NextApi/apiClient/historicalGraph?functionName=getIndexChart&&index=NIFTY%2050&flag=1Y

gold: https://www.nseindia.com/api/historical-spot-price?symbol=GOLD&fromDate=30-12-2024&toDate=30-12-2025

 https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getAllIndicesSymbols&&index=NIFTY%2050

https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getAllIndices

https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getIndexFacts&&index=NIFTY%2050

https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getFinancialResultGraph&&symbol=ADANIENT

 https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getShareHoldingData&&symbol=ADANIENT

https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getAnnouncementsIndices&flag=CAN&&index=NIFTY%2050

https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getMostActiveContracts&&index=NIFTY

https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getCorporateAction&&flag=CAC&&index=NIFTY%2050

https://www.nseindia.com/api/NextApi/apiClient/indexTrackerApi?functionName=getIndicesHeatMap&&index=NIFTY%2050


# format = '%Y-%m-%d%H:%M:%S'
# df['Datetime'] = pd.to_datetime(df['date'] + df['time'].astype("string"), format=format)
series_list = [series for col, series in df.items()]
"""

# Fetch data from NSE API
# import os
# import sys
# from pathlib import Path
from datetime import (datetime, timedelta)
import requests
import pandas as pd
import numpy as np


# sys.path.append(str(Path(os.getcwd()).parent.absolute()))
# sys.path.append(str(Path(os.getcwd()).absolute()))


class NSE_API():
    """
    helps to fetch data from NSE API
    """
    base_nse_url = "https://www.nseindia.com/"
    nse_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    def __init__(self):
        self.nse_session = requests.Session()
        self.nse_session.headers.update(self.nse_headers)
        self.nse_session.get(self.base_nse_url, headers=self.nse_headers,  timeout=10)
        self.nse_session.get(self.base_nse_url+"/option-chain", headers=self.nse_headers,  timeout=10)

    def _get_data(self, api_url, print_url=False):
        full_nse_api_url = self.base_nse_url + api_url

        if print_url:
            print(f"calling {full_nse_api_url} ..")

        output = dict()
        try:
            response = self.nse_session.get(full_nse_api_url)
            response.raise_for_status()
        except Exception as e:
            print(f"error from NSE_API.get_data(): {e}")
        else:
            if response.status_code == 200:
                output = response.json()
        return output


def get_nse_etf_data(symbol: str=None):
    """
    this function
    other nse api endpoints:
        - https://www.nseindia.com/api/etf
        - https://www.nseindia.com/api/quote-equity?symbol=GROWWDEFNC
        - https://www.nseindia.com/api/quote-equity?symbol=GROWWDEFNC&section=trade_info
    """
    nse_api = NSE_API()
    daily_nse_all_etfs_data = nse_api._get_data("api/etf").get('data')

    out = list()
    for item in daily_nse_all_etfs_data:
        if symbol is not None and item.get('symbol') != symbol:
            continue
        empty_dict = dict()
        etf_data = nse_api._get_data(f"api/quote-equity?symbol={item.get('symbol')}")

        # # imp: below code will be useful for further block deal and market depth data
        # etf_trade_info_data = nse_api._get_data(f"api/quote-equity?symbol={item.get('symbol')}&section=trade_info")
        # print(etf_trade_info_data)

        empty_dict['symbol'] = item.get('symbol')

        # empty_dict['symbol'] = etf_data.get('info').get('symbol')
        # empty_dict['company_name'] = etf_data.get('info').get('companyName')
        empty_dict['asset_company'] = etf_data.get('info').get('companyName').split('-')[0]
        empty_dict['listingDate'] = etf_data.get('info').get('listingDate')
        empty_dict['segment'] = etf_data.get('info').get('segment')
        # empty_dict['is_debt_sec'] = etf_data.get('info').get('isDebtSec')
        # empty_dict['is_etf_sec'] = etf_data.get('info').get('isETFSec')
        # empty_dict['identifier'] = etf_data.get('info').get('identifier')
        # empty_dict['is_top10'] = etf_data.get('info').get('isTop10')
        empty_dict['surveillance'] = etf_data.get('securityInfo').get('surveillance').get('surv')
        empty_dict['face_value'] = etf_data.get('securityInfo').get('faceValue')
        empty_dict['issued_size'] = etf_data.get('securityInfo').get('issuedSize')
        empty_dict['expense_ratio'] = ''  # np.nan

        empty_dict['toal_market_cap'] = round((etf_data.get('securityInfo').get('issuedSize') * etf_data.get('priceInfo').get('lastPrice')) / 10000000, 2)

        empty_dict['open'] = etf_data.get('priceInfo').get('open')
        empty_dict['high'] = etf_data.get('priceInfo').get('intraDayHighLow').get('max')
        empty_dict['low'] = etf_data.get('priceInfo').get('intraDayHighLow').get('min')
        empty_dict['close'] = etf_data.get('priceInfo').get('close')
        empty_dict['ltp'] = etf_data.get('priceInfo').get('lastPrice')

        empty_dict['trade_volume'] = item.get('qty')
        empty_dict['trade_value'] = item.get('trdVal')

        empty_dict['vwap'] = etf_data.get('priceInfo').get('vwap')
        empty_dict['previous_close'] = etf_data.get('priceInfo').get('previousClose')
        empty_dict['day_percentage_change'] = round(etf_data.get('priceInfo').get('pChange'),2)
        empty_dict['inav_value'] = etf_data.get('priceInfo').get('iNavValue')
        empty_dict['52week_high'] = etf_data.get('priceInfo').get('weekHighLow').get('max')
        empty_dict['52week_high_date'] = etf_data.get('priceInfo').get('weekHighLow').get('maxDate')
        empty_dict['52week_low'] = etf_data.get('priceInfo').get('weekHighLow').get('min')
        empty_dict['52week_low_date'] = etf_data.get('priceInfo').get('weekHighLow').get('minDate')

        empty_dict['yearly_percentage_change'] = item.get('perChange365d')
        empty_dict['monthly_percentage_change'] = item.get('perChange30d')

        empty_dict['last_update_time'] = etf_data.get('metadata').get('lastUpdateTime')
        	
        out.append(empty_dict)
    
    out_df = pd.DataFrame(out)
    # return out_df.reset_index(drop=True)
    return out


def get_nse_etf_data_ohlc(symbol: str, from_dt: str=None, to_dt: str=None):
    """
    this function
    other nse api endpoints:
        - https://www.nseindia.com/api/historicalOR/cm/equity?symbol=MODEFENCE
        - https://www.nseindia.com/api/historicalOR/generateSecurityWiseHistoricalData?from=17-11-2024&to=17-11-2025&symbol=MODEFENCE&type=priceVolumeDeliverable&series=ALL 
    """
    nse_api = NSE_API()
    if from_dt is None or to_dt is None:
        etf_data_monthly_ohlc = nse_api._get_data(f'api/historicalOR/cm/equity?symbol={symbol}')

        etf_data_monthly_ohlc_df = pd.DataFrame(etf_data_monthly_ohlc.get('data'))

        etf_data_monthly_ohlc_df.drop(columns=['CH_SERIES', 'TIMESTAMP', 'mTIMESTAMP', 'CH_TOT_TRADED_VAL', 'CH_52WEEK_HIGH_PRICE',	'CH_52WEEK_LOW_PRICE', 'SLBMH_TOT_VAL'], inplace=True)

        etf_data_monthly_ohlc_df.rename(columns={'CH_SYMBOL': 'symbol', 'CH_TIMESTAMP': 'timestamp', 'CH_PREVIOUS_CLS_PRICE': 'previous_close', 'CH_OPENING_PRICE': 'open', 'CH_TRADE_HIGH_PRICE': 'high', 'CH_TRADE_LOW_PRICE': 'low', 'CH_LAST_TRADED_PRICE': 'close', 'CH_CLOSING_PRICE': 'ltp', 'VWAP': 'vwap', 'CH_TOT_TRADED_QTY': 'volume', 'CH_TOTAL_TRADES': 'trades'}, inplace=True)

        etf_data_monthly_ohlc_df['timestamp'] = pd.to_datetime(etf_data_monthly_ohlc_df['timestamp'], format='%Y-%m-%d')

    elif from_dt is not None and to_dt is not None:
        etf_data_monthly_ohlc = nse_api._get_data(f'api/historicalOR/generateSecurityWiseHistoricalData?from={from_dt}&to={to_dt}&symbol={symbol}&type=priceVolumeDeliverable&series=ALL')

        etf_data_monthly_ohlc_df = pd.DataFrame(etf_data_monthly_ohlc.get('data'))

        etf_data_monthly_ohlc_df.drop(columns=['CH_SERIES', 'mTIMESTAMP', 'CH_TOT_TRADED_VAL', 'COP_DELIV_QTY', 'COP_DELIV_PERC'], inplace=True)

        etf_data_monthly_ohlc_df.rename(columns={'CH_SYMBOL': 'symbol', 'CH_TIMESTAMP': 'timestamp', 'CH_PREVIOUS_CLS_PRICE': 'previous_close', 'CH_OPENING_PRICE': 'open', 'CH_TRADE_HIGH_PRICE': 'high', 'CH_TRADE_LOW_PRICE': 'low', 'CH_LAST_TRADED_PRICE': 'close', 'CH_CLOSING_PRICE': 'ltp', 'VWAP': 'vwap', 'CH_TOT_TRADED_QTY': 'volume', 'CH_TOTAL_TRADES': 'trades'}, inplace=True)

    return etf_data_monthly_ohlc_df


def load_etf_data():
    final_etf_df_new = get_nse_etf_data().copy()

    final_etf_df_new_filtered = final_etf_df_new[(final_etf_df_new['asset_company'].str.contains('Motilal Oswal Mutual Fund', case=False, na=False)) | (final_etf_df_new['asset_company'].str.contains('DSP Mutual Fund', case=False, na=False)) | (final_etf_df_new['asset_company'].str.contains('ICICI Prudential Mutual Fund', case=False, na=False)) | (final_etf_df_new['asset_company'].str.contains('Nippon India Mutual Fund', case=False, na=False)) | (final_etf_df_new['asset_company'].str.contains('Aditya Birla Sun Life Mutual Fund', case=False, na=False)) | (final_etf_df_new['asset_company'].str.contains('AXIS MUTUAL FUND', case=False, na=False)) | (final_etf_df_new['asset_company'].str.contains('Mirae Asset Mutual Fund', case=False, na=False))]

    return final_etf_df_new_filtered.reset_index(drop=True)


def get_nse_market_status_daily():
    out_dict = dict()
    nse_api = NSE_API()
    nse_market_status = nse_api._get_data('api/marketstatus')
    # nse_market_status_df = pd.DataFrame(nse_market_status.get('marketState'))

    out_dict['nifty50_close'] = nse_market_status.get('indicativenifty50').get('closingValue')
    out_dict['nifty50_change'] = nse_market_status.get('indicativenifty50').get('change')
    out_dict['nifty50_perchange'] = nse_market_status.get('indicativenifty50').get('perChange')
    out_dict['nifty50_status'] = nse_market_status.get('indicativenifty50').get('status')
    out_dict['giftnifty_close'] = nse_market_status.get('giftnifty').get('LASTPRICE')
    out_dict['giftnifty_change'] = nse_market_status.get('giftnifty').get('DAYCHANGE')
    out_dict['giftnifty_perchange'] = nse_market_status.get('giftnifty').get('PERCHANGE')
    out_dict['marketcapin_trdollars'] = nse_market_status.get('marketcap').get('marketCapinTRDollars')
    out_dict['marketcapin_laccr_rupees'] = nse_market_status.get('marketcap').get('marketCapinLACCRRupees')
    out_dict['as_of_date'] = nse_market_status.get('indicativenifty50').get('dateTime')
    out_dict['current_date_time'] = nse_market_status.get('giftnifty').get('TIMESTMP')

    nse_market_status_df = pd.DataFrame(out_dict, index=[0])
    return nse_market_status_df


def get_nse_index_daily():
    nse_api = NSE_API()
    nse_index_daily = nse_api._get_data('api/NextApi/apiClient?functionName=getIndexData&&type=All')
    nse_index_daily_df = pd.DataFrame(nse_index_daily.get('data'))
    nse_index_daily_df.drop(columns=['timeVal', 'constituents', 'indicativeClose', 'icChange', 'icPerChange', 'isConstituents'], inplace=True)
    nse_index_daily_df.rename(columns={'indexName': 'index_name', 'previousClose': 'previous_close', 'percChange': 'perchange', 'yearHigh': '52week_high', 'yearLow': '52week_low'}, inplace=True)
    return nse_index_daily_df


def get_nse_india_vix(from_dt: str=None, to_dt: str=None):
    nse_api = NSE_API()
    df_list = list()

    if from_dt and to_dt:
        to_dt = datetime.strptime(to_dt, '%Y-%m-%d')
        from_dt = datetime.strptime(from_dt, '%Y-%m-%d')
    else:
        to_dt = datetime.now()
        from_dt = to_dt - timedelta(days=365)
        
    while from_dt < to_dt:
        from_dt_30 =  (to_dt - timedelta(days=30))
        nse_india_vix = nse_api._get_data(f'api/historicalOR/vixhistory?from={from_dt_30.strftime("%d-%m-%Y")}&to={to_dt.strftime("%d-%m-%Y")}')
        df_list.append(pd.DataFrame(nse_india_vix.get('data')))
        # print(from_dt_30, to_dt)
        to_dt = (from_dt_30 - timedelta(days=1))
        
    nse_india_vix_df = pd.concat(df_list[::-1], ignore_index=True)

    nse_india_vix_df.drop(columns=['EOD_INDEX_NAME'], inplace=True)
    nse_india_vix_df.rename(columns={'EOD_TIMESTAMP': 'date', 'EOD_OPEN_INDEX_VAL': 'open',	'EOD_HIGH_INDEX_VAL': 'high', 'EOD_LOW_INDEX_VAL': 'low', 'EOD_CLOSE_INDEX_VAL': 'close', 'EOD_PREV_CLOSE': 'previous_close', 'VIX_PTS_CHG': 'pts_change', 'VIX_PERC_CHG': 'perchange'}, inplace=True)
    # nse_india_vix_df.sort_values(by='date', ascending=True).reset_index(drop=True)
    return nse_india_vix_df


def get_nse_date():
    nse_api = NSE_API()
    nse_current_date = nse_api._get_data('api/NextApi/dynamicApi?functionName=getCurrentTime').get('data').get('currentTime')
    return nse_current_date


def load_graph_data_to_df(object: dict):
    identifier = object.get('data').get('identifier')
    # name = objecct.get('data').get('name')
    grapth_data = object.get('data').get('grapthData')
    df = pd.DataFrame(grapth_data, columns=['Timestamp', 'Price', 'Code'])
    df['Date'] = pd.to_datetime(df['Timestamp'], unit='ms')
    return df, identifier


if __name__ == '__main__':
    nse_api = NSE_API()
    daily_nse_all_etfs_data = nse_api._get_data("api/etf").get('data')

    # out = get_nse_etf_data()
    # out = get_nse_etf_data(symbol='MODEFENCE')

    # out = get_nse_etf_data_ohlc(symbol='MODEFENCE')
    # out = get_nse_etf_data_ohlc(symbol='MODEFENCE', from_dt='17-11-2024', to_dt='17-11-2025')

    # out = get_nse_market_status_daily()
    # out = get_nse_index_daily()

    # out = get_nse_india_vix()
    # out = get_nse_india_vix(from_dt='22-11-2024', to_dt='18-11-2025')

    # out = get_nse_date()
    print(daily_nse_all_etfs_data)
