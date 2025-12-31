import requests
import pandas as pd


def fetch_fii_dii_data(year:str="2025"):
    # url = "https://uapi.equitypandit.com/serve/api/v1/explore/cash-fii-dii-activity?year=2025&month=11"
    url = f"https://uapi.equitypandit.com/serve/api/v1/explore/cash-fii-dii-activity?year={year}"
    response = requests.get(url)
    df = pd.DataFrame(response.json()['data'])
    df = df.loc[df['date'] != 'Month till date', ['date', 'fiiNet', 'diiNet']]
    df['date'] = pd.to_datetime(df['date'], format="%Y-%m-%d")
    df.rename(columns={'date': 'Date', 'fiiNet': 'FII Net', 'diiNet': 'DII Net'}, inplace=True)
    return df


if __name__ == "__main__":
    data = fetch_fii_dii_data()
    print(data)
    