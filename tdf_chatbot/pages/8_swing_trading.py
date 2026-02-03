
import streamlit as st
from src.streamlit_side_navbar import render_sidebar
from src.market_data_fetcher import reits_invits
from src.async_market_data_fetcher import nifty_500_index_list, streamlit_market_overview, streamlit_nifty_stock_screener

st.set_page_config(page_title="Overview", layout="wide")

render_sidebar()

# df = sourcing_nifty_index_data(nifty_500_index_list)
nifty_tupple = streamlit_market_overview(nifty_500_index_list)

if 'nifty_sector_df' not in st.session_state:
    st.session_state['nifty_sector_df'] = nifty_tupple[0]
if 'nifty_index_constituents_df' not in st.session_state:
    st.session_state['nifty_index_constituents_df'] = nifty_tupple[1]
if 'nifty_500_index_stocks_df' not in st.session_state:
    st.session_state['nifty_500_index_stocks_df'] = nifty_tupple[3]

nifty_sector_df = st.session_state['nifty_sector_df']
sector_tabs_list = nifty_sector_df['key'].unique().tolist()

nifty_index_constituents_df = st.session_state['nifty_index_constituents_df']
nifty_500_stocks_list = nifty_tupple[2]

st.header("Market Overview")

st.divider()
st.markdown(f"### 🚀 Nifty Sectorial Data")
# col_sector, col_year, col_month, col_week, col_previous_day, col_current = st.columns(6)
with st.expander("See Nifty Sectorial Data"):
    tab_sectors = st.tabs(sector_tabs_list)
    for i, tab in enumerate(tab_sectors):
        with tab:
            filtered_nifty_sectorial_df = nifty_sector_df.loc[nifty_sector_df['key'] == sector_tabs_list[i],  \
                                        ["Index", "LTP", "%CHNG", "OPEN", "HIGH", "LOW", "PREV CLOSE", "52W H", "52W L", 
                                        "365D %CHNG", "30D %CHNG", "365D DATE", "30D DATE", "PREV DAY", "1W AGO", 
                                        "1M AGO VAL", "1W AGO VAL", "1Y AGO VAL","PREV DAY VAL"]].reset_index(drop=True)
            with st.expander("Nifty Sectorial Data", expanded=True):
                date_365d = filtered_nifty_sectorial_df["365D DATE"].iloc[0]  # e.g., "29-Jan-2025"
                date_30d = filtered_nifty_sectorial_df["30D DATE"].iloc[0]    # e.g., "30-Dec-2025"
                date_1w = filtered_nifty_sectorial_df["1W AGO"].iloc[0]       # e.g., "23-Jan-2026"
                date_prev = filtered_nifty_sectorial_df["PREV DAY"].iloc[0]   # e.g., "30-Jan-2026"

                col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 1, 1])
                with col1:
                    st.markdown("")
                    st.markdown(f"**Index**")
                with col2:
                    st.markdown(f"**Last 1 Year**")
                    st.markdown(f"**({date_365d})**")
                with col3:
                    st.markdown(f"**Last 1 Month**")
                    st.markdown(f"**({date_30d})**")
                with col4:
                    st.markdown(f"**Last 1 Week**")
                    st.markdown(f"**({date_1w})**")
                with col5:
                    st.markdown(f"**Prev Day**")
                    st.markdown(f"**({date_prev})**")
                with col6:
                    st.markdown("")
                    st.markdown(f"**LTP**")
                st.divider() # Adds a visual line below headers

                for index, row in filtered_nifty_sectorial_df.iterrows():
                    c1, c2, c3, c4, c5, c6 = st.columns([2, 1, 1, 1, 1, 1])
                    
                    with c1:
                        c1.write(row["Index"])
                    with c2:
                        # 1Y AGO VAL
                        c2.markdown(f":{'green' if row['LTP'] >= row['1Y AGO VAL'] else 'red'}[{row['1Y AGO VAL']:.2f}]") 
                    with c3:
                        # 1M AGO VAL
                        c3.markdown(f":{'green' if row['LTP'] >= row['1M AGO VAL'] else 'red'}[{row['1M AGO VAL']:.2f}]")
                    with c4:
                        # 1W AGO VAL
                        c4.markdown(f":{'green' if row['LTP'] >= row['1W AGO VAL'] else 'red'}[{row['1W AGO VAL']:.2f}]")
                    with c5:
                        # PREV DAY VAL
                        c5.markdown(f":{'green' if row['LTP'] >= row['PREV DAY VAL'] else 'red'}[{row['PREV DAY VAL']:.2f}]")
                    with c6:
                        # LTP (Current Value)
                        c6.write(f"**{row['LTP']:.2f}**")
            with st.expander("See Data explanation of Nifty Sectorial Data", expanded=False):
                st.dataframe(filtered_nifty_sectorial_df, width='stretch')


st.divider()
st.markdown(f"### 🚀 Nifty Index Data")
with st.expander("See Data explanation of Nifty Index Data"):
    tabs = st.tabs(nifty_500_index_list)
    for i, tab in enumerate(tabs):
        with tab:
            st.markdown(f"{nifty_500_index_list[i]} Data")
            styled_df = nifty_index_constituents_df.loc[nifty_index_constituents_df['Index'] == nifty_500_index_list[i], 
                        ["Symbol", "Weightage(%)", "LTP", "CHNG", "%CHNG", "VOLUME (in Lakhs)", "VALUE (in Cr)"]]  \
                        .reset_index(drop=True)  \
                        .style.background_gradient(
                            subset=["%CHNG"], 
                            cmap="RdYlGn", 
                            vmin=-2, 
                            vmax=2
                        ).format({"LTP": "{:.2f}%", "CHNG": "{:.2f}%", "%CHNG": "{:.2f}%"})
            st.dataframe(styled_df, width='stretch')


st.divider()
st.markdown(f"### 🚀 Nifty500 Stocks Screener")
with st.expander("See Nifty500 Stocks Screener"):
    nifty_500_index_stocks_df = st.session_state['nifty_500_index_stocks_df']
    selection = st.segmented_control(
        "Nifty Index", nifty_500_index_list, selection_mode="single"
    )
    if selection:
        st.markdown(f"Your selected options: {selection}.")
        nse_stock_price_info_df = streamlit_nifty_stock_screener(nifty_500_index_stocks_df, selection)
        st.dataframe(nse_stock_price_info_df.loc[:, :].reset_index(drop=True), width="stretch")


st.divider()
st.markdown("### 🚀 Nifty REIT & INVIT")
with st.expander("See Nifty REIT & INVIT"):
    st.dataframe(reits_invits())