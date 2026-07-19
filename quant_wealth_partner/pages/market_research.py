import streamlit as st
import pandas as pd
from io import StringIO
from utilities.stocks.fetch_india_stocks import (fetch_all_indices_data, 
                                                 fetch_market_watch_index_data,
                                                 help_fetch_screener_data,
                                                 fetch_company_info)

st.header("Market Research Tools")

screener_dict = {
    "FII Buying": "https://www.screener.in/screens/343087/fii-buying/",
    "PAT > 0 in qtr": "https://www.screener.in/screens/608536/all-latest-quarterly-results/",
    "Debt Free": "https://www.screener.in/screens/1/debt-free/",
    "High ROE": "https://www.screener.in/screens/2/high-roe/",
    "Value Stocks": "https://www.screener.in/screens/3/value-stocks/",
}

if "market_watch_index" not in st.session_state:
    st.session_state.market_watch_index = False
    st.session_state.market_watch_index_df = pd.DataFrame()
    
if "active_screen_data" not in st.session_state:
    st.session_state.active_screen_info = {'name': None, 'url': None}
    st.session_state.active_screen_data = pd.DataFrame()

if "active_scrip" not in st.session_state:
    st.session_state.active_scrip = "500325" # Default: Reliance Industries

if "bse_data_store" not in st.session_state:
    st.session_state.bse_data_store = {
        "Company Market Data": None,
        "Financials (Income Statement)": None,
        "Annual Report": None,
        "Corporate Actions": None
    }

# This runs instantly when a button is clicked, BEFORE the rest of the script reruns
def handle_button_click_for_screeners(name: str, url: str):
    st.session_state.active_screen_info['name'] = name
    st.session_state.active_screen_info['url'] = url
    st.session_state.active_screen_data = help_fetch_screener_data(url.strip())

SCREENER_BUTTONS_PER_ROW = 8
screener_items = list(screener_dict.items())


# 1. Source DataFrame
all_indices_df = fetch_all_indices_data()
unique_keys = all_indices_df["key"].unique().tolist()

# 5. Tabs for each unique key
st.subheader("👉 Sectorial and Thematic Indices Analysis:")
tabs = st.tabs(unique_keys)

# Loop over keys and tabs together to render filtered content
for key, tab in zip(unique_keys, tabs):
    with tab:
        st.subheader(f"{key}")

        # Filter DataFrame for the current key
        filtered_df_for_key_tab = all_indices_df.loc[(all_indices_df["key"] == key), ['index', 'open', 'high', 'low', 'last', 'variation', 
                                                    'percentChange',  'yearHigh', 'yearLow', 'pe', 'pb', 'dy', 'previousDayVal', 
                                                    'oneWeekAgoVal', 'oneMonthAgoVal', 'perChange30d', 'oneYearAgoVal', 'perChange365d']].reset_index(drop=True)

        # Display the filtered DataFrame
        st.dataframe(filtered_df_for_key_tab, width='stretch')


st.divider()
with st.expander("👉 Choose Group and Specific Indices For Further Analysis"):
    col1, col2 = st.columns(2)

    # 2. 1st Dropdown: Select 'key'
    # unique_keys = all_indices_df["key"].unique().tolist()
    with col1:
        selected_key = st.selectbox("Select Key", options=unique_keys)

    # 3. Filter DataFrame based on 1st selection (key)
    filtered_df_by_key = all_indices_df[all_indices_df["key"] == selected_key]

    # 4. 2nd Dropdown: Select 'index' (Dependent on 1st dropdown)
    unique_indices = filtered_df_by_key["index"].unique().tolist()
    with col2:
        selected_index = st.selectbox("Select Index", options=unique_indices)

    # Fetch the specific row matching both selections
    filtered_df_by_key_index_01 = all_indices_df.loc[(all_indices_df["key"] == selected_key) & (all_indices_df["index"] == selected_index),
                                                    ['index', 'open', 'high', 'low', 'last', 'variation', 'percentChange',  'yearHigh', 'yearLow', 
                                                    'pe', 'pb', 'dy']]
    filtered_df_by_key_index_02 = all_indices_df.loc[(all_indices_df["key"] == selected_key) & (all_indices_df["index"] == selected_index),
                                                    ['index', 'previousDay', 'previousDayVal', 'oneWeekAgo', 'oneWeekAgoVal', 'date30dAgo', 'oneMonthAgoVal', 'perChange30d', 
                                                    'date365dAgo', 'oneYearAgoVal', 'perChange365d']]

    st.dataframe(filtered_df_by_key_index_01, width='stretch', hide_index=True)
    st.dataframe(filtered_df_by_key_index_02, width='stretch', hide_index=True)

    # 6. Submit Button
    if st.button("Submit", type="primary"):
        selected_index = all_indices_df[all_indices_df['index'] == selected_index]['indexSymbol'].item().replace(' ', '%20')
        st.session_state.market_watch_index_df = fetch_market_watch_index_data(selected_index)
        st.session_state.market_watch_index = True
        st.success(f"Submitted! Key: **{selected_key}** | Index: **{selected_index}**")

    if st.session_state.market_watch_index:
        st.write("Select Multi-row to view the Market Watch Index Data. Extras: Value (in Crores), Volume (in Lakhs), Floating_MCap (in Crores)")
        selection_event = st.dataframe(st.session_state.market_watch_index_df, width='stretch', on_select="rerun", selection_mode=["multi-row"])  #{'single-row-required', 'multi-column', 'single-row', 'single-column', 'multi-cell', 'single-cell', 'multi-row'}

        selected_indices = selection_event.selection.rows
        if selected_indices:
            selected_companies = st.session_state.market_watch_index_df.iloc[selected_indices]["symbol"].tolist()
            
            st.success(f"You have selected {len(selected_companies)} companies for further analysis.")
            st.markdown(f"Further analysis for: {', '.join(selected_companies)}")
        else:
            st.info("Awaiting selection...")


st.divider()
with st.expander("⚡ Dynamic Screeners From Screener.com"):
    screener_tabs = st.tabs(["Screens From Screener.com", "FII Buying From EquityMaster.com"])
    for tab in screener_tabs:
        with tab:
            if tab == screener_tabs[0]:
                st.markdown("Other Screenes from Screener.com is available [here](https://www.screener.in/screens/).")

                # Screener Buttons
                for i in range(0, len(screener_items), SCREENER_BUTTONS_PER_ROW):
                    chunk = screener_items[i : i + SCREENER_BUTTONS_PER_ROW]
                    cols = st.columns(SCREENER_BUTTONS_PER_ROW)
                    for col, (name, url) in zip(cols, chunk):
                        with col:
                            st.button(
                                label=name,
                                key=f"btn_{name}",
                                on_click=handle_button_click_for_screeners,
                                args=(name, url), # Passes these variables into the callback function
                                width='stretch' # Stretches the button to fill the column cleanly
                            )

                with st.form("screener_form"):
                    target_url = st.text_input(
                        "Enter Screener.in URL",
                        value = st.session_state.active_screen_info['url']
                    )
                    submitted = st.form_submit_button("Fetch Data", type="primary")
                if submitted:
                    if target_url.strip():
                        with st.spinner("Scraping paginated data via Async I/O..."):
                            result_df = help_fetch_screener_data(target_url.strip())
                            if not result_df.empty:
                                st.session_state.active_screen_info['name'] = "Other Screener"
                                st.session_state.active_screen_info['url'] = target_url.strip()
                                st.session_state.active_screen_data = result_df
                            else:
                                st.warning("No data found. Verify the URL or check if the screen is empty.")
                    else:
                        st.error("Please enter a valid URL.")

                if not st.session_state.active_screen_data.empty:
                    st.success(f"Successfully extracted {len(st.session_state.active_screen_data)} companies.")
                    st.markdown(f"📊 Cached Market Screen from [{st.session_state.active_screen_info['name']}]({st.session_state.active_screen_info['url']})")
                    st.markdown(f"Successfully extracted {len(st.session_state.active_screen_data)} companies.")
                    st.dataframe(
                        st.session_state.active_screen_data,
                        width='stretch',
                        # hide_index=True,
                    )
            else:
                st.markdown("This screener fetches data from [EquityMaster.com](https://www.equitymaster.com/stock-market/fii-portfolio/) for FII buying activity.")
        

st.divider()
st.subheader("👉 Specific Stock Data Analysis -")
st.divider()
with st.expander("👉 Fundamental Analysis:"):
    with st.form("bse_search_form"):
        input_scrip = st.text_input(
            "Enter BSE Scrip Code", 
            value=st.session_state.active_scrip
        )
        submitted = st.form_submit_button("Fetch Data", type="primary")

    if submitted:
        clean_scrip = input_scrip.strip()
        if clean_scrip:
            if clean_scrip != st.session_state.active_scrip:
                st.session_state.active_scrip = clean_scrip
                st.session_state.bse_data_store = {
                    "Company Market Data": None,
                    "Financials (Income Statement)": None,
                    "Annual Report": None,
                    "Corporate Actions": None
                }
        else:
            st.error("Please enter a valid scrip code.")
    
    selected_tab = st.radio(
        "Select Data Category:",
        ["Company Market Data", "Financials (Income Statement)", "Annual Report", "Corporate Actions"],
        horizontal=True,
        label_visibility="collapsed" # Hides the label for a cleaner tab look
    )

    # if selected_tab:
    if st.session_state.active_scrip:
        if st.session_state.bse_data_store[selected_tab] is None:
            with st.spinner(f"Fetching {selected_tab} for {st.session_state.active_scrip} from BSE..."):
                raw_data = fetch_company_info(selected_tab, st.session_state.active_scrip)
                st.session_state.bse_data_store[selected_tab] = raw_data
        
        st.subheader(f"{selected_tab}")
        if selected_tab == "Financials (Income Statement)":
            qtr_tab, yr_tab = st.tabs(["Quaterly Financials (Income Statement)", "Annual Financials (Income Statement)"])
            with qtr_tab:
                st.dataframe(st.session_state.bse_data_store[selected_tab][0])
            with yr_tab:
                st.dataframe(st.session_state.bse_data_store[selected_tab][1])
        else:
            st.dataframe(st.session_state.bse_data_store[selected_tab], width="stretch")


st.divider()
st.subheader("👉 Other Research Tools")
st.markdown("[NISM News letter](https://www.nism.ac.in/newsletter-2026/)")
st.markdown("[NSE Corporate Action](https://www.nseindia.com/companies-listing/corporate-filings-insider-trading)")