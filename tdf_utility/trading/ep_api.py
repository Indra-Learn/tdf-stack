from datetime import datetime as dt, timedelta as td
import requests
import pandas as pd


# def fetch_fii_dii_data(year:str="2025"):
#     # url = "https://uapi.equitypandit.com/serve/api/v1/explore/cash-fii-dii-activity?year=2025&month=11"
#     url = f"https://uapi.equitypandit.com/serve/api/v1/explore/cash-fii-dii-activity?year={year}"
#     response = requests.get(url)
#     df = pd.DataFrame(response.json()['data'])
#     df = df.loc[df['date'] != 'Month till date', ['date', 'fiiNet', 'diiNet']]
#     df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")
#     df.rename(columns={'date': 'Date', 'fiiNet': 'FII Net', 'diiNet': 'DII Net'}, inplace=True)
#     return df


def fetch_fii_dii_data(year:str=None):
    # url = "https://uapi.equitypandit.com/serve/api/v1/explore/cash-fii-dii-activity?year=2025&month=11"
    df_list = []
    if year:
        url = f"https://uapi.equitypandit.com/serve/api/v1/explore/cash-fii-dii-activity?year={year}"
        response = requests.get(url)
        df = pd.DataFrame(response.json()['data'])
        df_list.append(df)
    else: # last 1 year
        to_dt = dt.now()
        from_dt = to_dt - td(days=390)
        result_list = []
        current_year = from_dt.year
        current_month = from_dt.month

        target_year = to_dt.year
        target_month = to_dt.month

        # 3. Loop until we pass the target year/month
        while (current_year < target_year) or (current_year == target_year and current_month <= target_month):
            result_list.append((current_year, current_month))
    
            # Increment month
            current_month += 1
            # Handle year rollover
            if current_month > 12:
                current_month = 1
                current_year += 1

        for year, month in result_list:
            url = f"https://uapi.equitypandit.com/serve/api/v1/explore/cash-fii-dii-activity?year={year}&month={month}"
            response = requests.get(url)
            df = pd.DataFrame(response.json()['data'])
            df_list.append(df)
    
    final_df = pd.concat(df_list)
    final_df = final_df.loc[final_df['date'] != 'Month till date', ['date', 'fiiNet', 'diiNet']]
    final_df['date'] = pd.to_datetime(final_df['date'], format="%Y-%m-%d")
    final_df.rename(columns={'date': 'Date', 'fiiNet': 'FII Net', 'diiNet': 'DII Net'}, inplace=True)
    # final_df.sort_values(by='Date', inplace=True)
    return final_df


if __name__ == "__main__":
    data = fetch_fii_dii_data()
    print(data)
    