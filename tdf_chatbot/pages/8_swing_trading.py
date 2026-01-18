import streamlit as st
from datetime import datetime as dt
from src.streamlit_side_navbar import render_sidebar
from src.market_data_fetcher import get_nifty_index_data, reits_invits

st.set_page_config(page_title="Market Analysis", layout="wide")

render_sidebar()

st.subheader("Swing Trading")


indices = ["REIT & INVIT", "NIFTY 50", "NIFTY NEXT 50", "NIFTY MIDCAP 150", "NIFTY SMLCAP 250"]  # prod - uncomment
# indices = ["REIT & INVIT", "NIFTY 50"]
tabs = st.tabs(indices)
for i, tab in enumerate(tabs):
    with tab:
        st.markdown(f"### 🚀 {indices[i]}")

        if indices[i] == "REIT & INVIT":
            # Nifty REITs & InvITs index
            st.dataframe(reits_invits())
        else:
            # start_time = dt.now()
            nifty_date, nifty_index_stocks_df, stock_yearly_df, stock_monthly_df = get_nifty_index_data(nifty_index_symbol=indices[i])

            selected_df1 = st.dataframe(nifty_index_stocks_df,
                            # hide_index=True,
                            use_container_width=True,
                            height=300)

            st.divider()
            st.markdown(f"### 🚀 Yearly Data")

            selected_df = st.dataframe(stock_yearly_df.loc[stock_yearly_df['Date'] == nifty_date, ["Symbol", "Date", "Close", "52Week High", "52Week High Date", "52Week Low", "52Week Low Date"]],
                            # hide_index=True,
                            use_container_width=True,
                            height=300,
                            key=f"editor_{indices[i]}", # Unique key for each tab
                            selection_mode="single-row",
                            on_select="rerun")
            
            st.divider()
            selected_ticker = ""
            if len(selected_df.selection["rows"]) > 0:
                # Get the selected row index
                selected_index = selected_df.selection["rows"][0]
                selected_ticker = nifty_index_stocks_df.iloc[selected_index]["Symbol"]
                st.markdown(f"### 🚀 Swing Trading Strategy for {selected_ticker}")

                st.dataframe(stock_monthly_df.loc[stock_monthly_df['Symbol'] == selected_ticker],
                            use_container_width=True,
                            height=300)
                st.divider()
                st.dataframe(stock_yearly_df.loc[stock_yearly_df['Symbol'] == selected_ticker],
                            use_container_width=True,
                            height=300)
            else:
                st.markdown("### 🚀 Select the stock from above table for Swing Trading")
                st.dataframe()

            
            # end_time = dt.now()
            # duration = end_time - start_time
            # st.sidebar.write(f"Fetching time: {duration/60} minutes")