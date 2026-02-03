import os
import time
import json
import pandas as pd
from NorenRestApiPy.NorenApi import  NorenApi
import pyotp
# import logging

# logging.basicConfig(level=logging.DEBUG)

class ShoonyaApiPy(NorenApi):
    def __init__(self):
        NorenApi.__init__(self, host='https://api.shoonya.com/NorenWClientTP/', websocket='wss://api.shoonya.com/NorenWSTP/')        
        global shoonya_api
        shoonya_api = self

shoonya_api = ShoonyaApiPy()

def shoonya_login() -> dict:
    #credentials
    uid     = os.getenv("SHOONYA_UID")
    pwd     = os.getenv("SHOONYA_PWD")
    factor2 = pyotp.TOTP(os.getenv("SHOONYA_TOTP_SECRET")).now()
    vc      = os.getenv("SHOONYA_VENDOR_CODE")
    app_key = os.getenv("SHOONYA_API_KEY")
    imei    = os.getenv("SHOONYA_IMEI")

    # Login
    shoonya_login_user = shoonya_api.login(userid=uid, password=pwd, twoFA=factor2, vendor_code=vc, api_secret=app_key, imei=imei)
    return shoonya_login_user

def shoonya_watchlists(shoonya_login_user: dict) -> pd.DataFrame:
    watchlists_list = []
    for key in shoonya_login_user.get('mws'):
        watchlist_df = pd.DataFrame(shoonya_login_user.get('mws').get(key))
        watchlist_df["watchlist_name"] = key
        watchlists_list.append(watchlist_df)
    watchlists_df = pd.concat(watchlists_list).reset_index(drop=True)
    return watchlists_df

def shoonya_limits() -> dict:
    limits = shoonya_api.get_limits()
    return limits

def shoonya_search_scrip(serch_text: str, tism_search: str, exchange: str='NSE') -> str:
    search_scrip_data = shoonya_api.searchscrip(exchange=exchange, searchtext=serch_text)
    search_scrip_df = pd.DataFrame(search_scrip_data.get('values'))
    token = None
    if not search_scrip_df.loc[search_scrip_df['tsym'] == tism_search, "token"].empty:
        token = search_scrip_df.loc[search_scrip_df['tsym'] == tism_search, "token"].values[0]
    return token

def get_time(time_string):
    data = time.strptime(time_string,'%d-%m-%Y %H:%M:%S')
    return int(time.mktime(data))


if __name__ == "__main__":
    shoonya_login_user = shoonya_login()
    shoonya_limits_dict = shoonya_limits()
    # shoonya_watchlists_df = shoonya_watchlists(shoonya_login_user)
    # nifty50_token = shoonya_search_scrip(serch_text="NIFTY", tism_search="Nifty 50", exchange="NSE")
