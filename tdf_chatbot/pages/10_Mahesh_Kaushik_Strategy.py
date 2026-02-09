import streamlit as st
import pandas as pd
from src.streamlit_side_navbar import render_sidebar
from src.async_fetch_nse_etf import (streamlit_nse_etf_trade_data, 
                                     streamlit_nse_etf_historical_openchart,
                                     streamlit_nse_etf_52wk_high_low)

st.set_page_config(page_title="Market Analysis", layout="wide")

render_sidebar()

final_etf_df = pd.DataFrame()

if 'nse_etf_trade_df' not in st.session_state:
    st.session_state['nse_etf_trade_df'] = streamlit_nse_etf_trade_data()
nse_etf_trade_df = st.session_state['nse_etf_trade_df']
nse_etf_symbols = nse_etf_trade_df['Symbol'].unique().tolist()

if 'nse_etf_historal_dma_df' not in st.session_state:
    st.session_state['nse_etf_historal_dma_df'] = st.session_state['nse_etf_historal_dma_df'] = streamlit_nse_etf_historical_openchart(nse_etf_symbols).loc[:, ['Symbol', '20DMA', '100DMA']]

if 'nse_etf_52wk_high_low_df' not in st.session_state:
    st.session_state['nse_etf_52wk_high_low_df'] = streamlit_nse_etf_52wk_high_low(nse_etf_symbols)

final_df_with_dma = pd.merge(nse_etf_trade_df, st.session_state['nse_etf_historal_dma_df'], left_on='Symbol', right_on='Symbol', how='inner')
final_df_with_52wk_data = pd.merge(final_df_with_dma, st.session_state['nse_etf_52wk_high_low_df'], left_on='Symbol', right_on='Symbol', how='inner')
final_df = final_df_with_52wk_data.copy()


st.subheader("ETFs Strategies")
st.html("<h4>🙏 Thanks to Mahesh Kaushik Sir, For Below ETF's Strategies</h4>")

with st.expander("ETF Screener With Assets, i-NAV, (**Filter out, volumn < 10000 & 'LIQUID'/'BOND'/'G-SEC'/'GILT' ETFS"):
    st.dataframe(final_df)

# ref_col1, ref_col2 = st.columns(2)
# with ref_col1:
#     if st.button("Refresh for 20DMA, 100DMA", icon="🔄", type="secondary"):
#         st.session_state['nse_etf_historal_dma_df'] = streamlit_nse_etf_historical_openchart(nse_etf_symbols).loc[:, ['Symbol', '20DMA', '100DMA']]
# with ref_col2:
#     if st.button("Refresh for 52Wk High Low Date", icon="🔄", type="secondary"):
#         st.session_state['nse_etf_52wk_high_low_df'] = streamlit_nse_etf_52wk_high_low(nse_etf_symbols)
# with st.expander("ETF Screener With 20DMA, 100DMA"):
#     st.dataframe(final_etf_df)


etf_strategies = [
    {
        "name": "Automated Share Screen Google Sheet (ETF)", 
        "short_descriptions": "Hold for months and look for profit of 10%", 
        "long_descriptions": "", 
        "conditions": ["ETFS's volume should greater than 5000", "Ignore Debt/Bond ETFs", "Current Market Price(CMP) should greater than 100DMA Price", "Current Market Price(CMP) should greater than by 20% of 6months lowest price", "Prev Close price should less than of 100DMA"],
        "required_details": ["CMP", "Prev Close", "100DMA", "Last 6months Minimum price"],
        "capital_requirements": ["If capital=150000, invest in stocks 150000/30=5000 at a time/stock and look for 10% of 5000 (500) profit booking"],
        "average_out_strategy": [],
        "youtube links": ["https://www.youtube.com/watch?v=mdD8w_TR73k&t=194s"]
    },
    {   
        "name": "ETF Ki Dukan",
        "short_descriptions": "Hold for few days to months and look for profit of 6%", 
        "long_descriptions": "",
        "conditions": [],
        "required_details": ["Underlying Asset", "CMP", "20DMA", "CMP-20DMA", "%change of 20DMA vs CMP", "Highest Down by %change of 20DMA"],
        "capital_requirements": ["If capital-200000, invest in ETFs 2lacs/60=3333 at a time/stock. Obviously we can invest 2lacs/10=20k directly in one ETF but to average out, we will further breakdown the amount 20k by 6=3333 for safe investment"],
        "average_out_strategy": [],
        "youtube links": ["https://youtu.be/1UJNwvBNKXk?si=D0vcItN_PSJEHUEx"]
    },
    {
        "name": "Alchemist Bidhi on ETF",
        "short_descriptions": "", 
        "long_descriptions": "",
        "conditions": [],
        "required_details": [],
        "capital_requirements": [],
        "average_out_strategy": [],
        "youtube links": []
    },
    {
        "name": "Paiso ka Ped (PKP) Nifty ETF",
        "short_descriptions": "", 
        "long_descriptions": "",
        "conditions": [],
        "required_details": [],
        "capital_requirements": [],
        "average_out_strategy": [],
        "youtube links": []
    },
    
]

strategy_names = [s['name'] for s in etf_strategies]
selected_name = st.segmented_control("Select a Strategy to View Details:", 
                                    strategy_names, 
                                    default=strategy_names[0],
                                    selection_mode='single')
if selected_name:
    strat = next(s for s in etf_strategies if s['name'] == selected_name)
    st.divider()
    col1, col2 = st.columns([2, 1])
    with col1:
        st.header(strat['name'])
        if strat['short_descriptions']:
            st.markdown(f"**Overview:** *{strat['short_descriptions']}*")
        if strat['long_descriptions']:
            st.caption(strat['long_descriptions'])
    st.write("---")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("✅ Entry Conditions")
        if strat['conditions']:
            for cond in strat['conditions']:
                st.markdown(f"- {cond}")
        else:
            st.info("No specific conditions listed.")

    with c2:
        st.subheader("📊 Required Data Points")
        if strat['required_details']:
            # Displaying as badges/labels
            st.write(" ".join([f"`{item}`" for item in strat['required_details']]))
        else:
            st.info("No data points defined.")

    st.write("")
    st.subheader("💰 Capital & Execution")
    cc1, cc2 = st.columns(2)
    
    with cc1:
        st.info("**Capital Allocation**\n\n" + "\n".join([f"- {i}" for i in strat['capital_requirements']]) if strat['capital_requirements'] else "No capital rules defined.")
        
    with cc2:
        st.warning("**Average-Out Strategy**\n\n" + "\n".join([f"- {i}" for i in strat['average_out_strategy']]) if strat['average_out_strategy'] else "Standard average-out rules apply.")

    # Block C: Learning Materials (YouTube)
    if strat['youtube links']:
        with st.expander("📺 Watch Video Tutorial"):
            for link in strat['youtube links']:
                st.video(link)
    else:
        st.caption("No video tutorial available for this strategy.")
else:
    st.warning("Please select a strategy from the menu above.")