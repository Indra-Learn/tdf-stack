import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import pytz
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe


@st.cache_resource
def init_gspread():
    """
    Initializes the Google Sheets connection securely using Streamlit Secrets.
    @st.cache_resource ensures the connection pool is reused across reruns.
    """
    creds_dict = dict(st.secrets["connections"]["gsheets"])
    sheet_url = creds_dict.get("spreadsheet")

    gc = gspread.service_account_from_dict(creds_dict)
    return gc, sheet_url

gc, target_sheet_url = init_gspread()

@st.cache_data(ttl=600) # Cache data for 10 minutes (600 seconds)
def read_sheet_data(sheet_name: str) -> pd.DataFrame:
    """
    Reads data into a Pandas DataFrame.
    """
    try:
        # sh = gc.open(SHEET_ID)
        sh = gc.open_by_url(target_sheet_url)

        worksheet = sh.worksheet(sheet_name)
        # get_as_dataframe handles blank rows and columns automatically
        # df = get_as_dataframe(worksheet, evaluate_formulas=True).dropna(how='all').dropna(axis=1, how='all')
        df = get_as_dataframe(worksheet, evaluate_formulas=True)
        df = df.replace(r'^\s*$', np.nan, regex=True)
        df = df.dropna(how='all')  # Drop rows where EVERY single column is NaN
        df = df.dropna(axis=1, how='all')  # Drop columns where EVERY single row is NaN
        return df
    except Exception as e:
        st.error(f"Failed to read data: {e}")
        return pd.DataFrame()
    
def write_sheet_data(sheet_name: str, df: pd.DataFrame):
    """
    Overwrites the specified worksheet with the provided DataFrame.
    """
    try:
        # sh = gc.open(SHEET_ID)
        sh = gc.open_by_url(target_sheet_url)

        worksheet = sh.worksheet(sheet_name)
        worksheet.clear() # Clear existing data
        
        # High-speed bulk write
        set_with_dataframe(worksheet, df, row=1, col=1, include_index=False)

        # gather audit metadata and load into status sheet
        num_rows = df.shape[0]
        num_cols = df.shape[1]
        ist_timezone = pytz.timezone('Asia/Kolkata')
        current_time = datetime.now(ist_timezone).strftime("%Y-%m-%d %H:%M:%S")
        log_record = [sheet_name, num_rows, num_cols, current_time]

        status_ws = sh.worksheet("Sheet_Status")
        # Look for the sheet_name strictly in Column 1 (Column A)
        cell = status_ws.find(sheet_name, in_column=1)
        # If found, update that specific row (Columns A through D)
        row_idx = cell.row
        # Note: Wrap log_record in another list [[]] because update expects a 2D matrix
        status_ws.update(f"A{row_idx}:D{row_idx}", [log_record])
        if not cell:
            # If the sheet_name doesn't exist in the log yet, append it normally
            status_ws.append_row(log_record)
        # Clear the read cache so the UI shows the latest data on next refresh
        read_sheet_data.clear() 
        return True
    except Exception as e:
        st.error(f"Failed to write data: {e}")
        return False