import streamlit as st
from datetime import datetime as dt
from src.streamlit_side_navbar import render_sidebar
from src.market_data_fetcher import get_nifty_index_data

st.set_page_config(page_title="Market Analysis", layout="wide")

render_sidebar()

st.subheader("Swing Trading inspired by Mahesh Kaushik Sir")

indices = ["REIT & INVIT", "NIFTY 50", "NIFTY 100", "NIFTY LARGEMIDCAP 250"]
tabs = st.tabs(indices)
for i, tab in enumerate(tabs):
    with tab:
        st.markdown(f"### 🚀 {indices[i]} Swing Trade")

        if indices[i] == "REIT & INVIT":
            st.dataframe()
        else:
            start_time = dt.now()
            nifty_index_stocks_df, stock_df = get_nifty_index_data(nifty_index_symbol=indices[i])
            selected_df = st.dataframe(nifty_index_stocks_df,
                                        hide_index=True,
                                        use_container_width=True,
                                        height=500,
                                        key=f"editor_{indices[i]}", # Unique key for each tab
                                        selection_mode="single-row",
                                        on_select="rerun")
            st.divider()
            selected_ticker = ""
            if len(selected_df.selection["rows"]) > 0:
                # Get the selected row index
                selected_index = selected_df.selection["rows"][0]
                # selected_ticker = df.iloc[selected_index]["Symbol"]
            st.write(stock_df.columns)
            st.dataframe(stock_df.loc[stock_df['chSymbol'] == selected_ticker])

            # end_time = dt.now()
            # duration = end_time - start_time
            # st.sidebar.write(f"Fetching time: {duration/60} minutes")