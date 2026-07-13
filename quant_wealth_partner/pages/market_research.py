import streamlit as st
import pandas as pd
from utilities.stocks.fetch_india_stocks import fetch_all_indices_data, fetch_market_watch_index_data

st.header("Market Research Tools")

if "market_watch_index" not in st.session_state:
    st.session_state.market_watch_index = False
    st.session_state.market_watch_index_df = pd.DataFrame()

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
st.subheader("👉 Choose Group and Specific Indices For Further Analysis")

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
st.subheader("Other Research Tools")
st.markdown("[NISM News letter](https://www.nism.ac.in/newsletter-2026/)")
st.markdown("[NSE Corporate Action](https://www.nseindia.com/companies-listing/corporate-filings-insider-trading)")