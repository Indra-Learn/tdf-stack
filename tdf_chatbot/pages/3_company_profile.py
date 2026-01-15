import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from src.market_data_fetcher import company_viz_df
from src.streamlit_side_navbar import render_sidebar


st.set_page_config(page_title="Company Profile", layout="wide")

render_sidebar()

query_params = st.query_params
ticker_symbol = query_params.get("ticker_symbol", None)

if st.button("← Back to Analysis"):
    st.switch_page("pages/2_market_analysis.py")

if ticker_symbol:
    company_name, company_trade_data_df, company_corp_action_df = company_viz_df(company_ticker=ticker_symbol)
    st.header(f"🏢 Company Ticker: {ticker_symbol}")
    st.subheader(f"Fetching deep dive analysis for: **{company_name}**")
    
    # Here you would call your API/Database
    # data = get_stock_data(ticker)
    
    # Mock Data for demo
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Price", "₹2,450", "+1.2%")
    col2.metric("PE Ratio", "24.5", "-0.5")
    col3.metric("Sector", "Energy")

    # --======================================================================================
    fig_company = make_subplots(specs=[[{"secondary_y": True}]])

    # Add Trace 1: Nifty 50 (Left Axis)
    fig_company.add_trace(
        go.Scatter(
            x=company_trade_data_df['Date'], 
            y=company_trade_data_df['Close'], 
            name="close",
            line=dict(color="#FFFFFF", width=2)
        ),
        secondary_y=False, # Assign to primary (left) axis
    )

    fig_company.add_trace(
        go.Scatter(
            x=company_trade_data_df['Date'], 
            y=company_trade_data_df['High'], 
            name="high",
            line=dict(color="#FF0000", width=2)
        ),
        secondary_y=False, # Assign to primary (left) axis
    )

    fig_company.add_trace(
        go.Scatter(
            x=company_trade_data_df['Date'], 
            y=company_trade_data_df['Low'], 
            name="low",
            line=dict(color='#00C805', width=2)
        ),
        secondary_y=False, # Assign to primary (left) axis
    )

    # fig_nifty_indiavix.update_yaxes(title_text="<b>Nifty Price</b>", secondary_y=False)
    # fig_nifty_indiavix.update_yaxes(title_text="<b>VIX Level</b>", secondary_y=True)

    fig_company.update_layout(
        title=f"Company",
        # xaxis_title="Date",
        yaxis_title="Nifty50",
        template="plotly_dark", # Use 'plotly_white' for light theme
        hovermode="x unified",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )

    st.plotly_chart(fig_company, use_container_width=True)

    # --======================================================================================
    # 2. CREATE THE BASE CANDLESTICK CHART
    fig_company = go.Figure(data=[go.Candlestick(
        x=company_trade_data_df['Date'],
        open=company_trade_data_df['Open'],
        high=company_trade_data_df['High'],
        low=company_trade_data_df['Low'],
        close=company_trade_data_df['Close'],
        name="Price" # Legend name
    )])

    # 3. ADD THE 7 DMA LINE (Standard Color: Blue or Green)
    fig_company.add_trace(go.Scatter(
        x=company_trade_data_df['Date'],
        y=company_trade_data_df['7_DMA'],
        mode='lines',
        name='7 DMA',
        line=dict(color='blue', width=1.5)
    ))

    # 4. ADD THE 21 DMA LINE (Standard Color: Red or Black)
    fig_company.add_trace(go.Scatter(
        x=company_trade_data_df['Date'],
        y=company_trade_data_df['21_DMA'],
        mode='lines',
        name='21 DMA',
        line=dict(color='black', width=1.5)
    ))

    # 5. ADD THE VWAP Line
    fig_company.add_trace(
        go.Scatter(
            x=company_trade_data_df['Date'], 
            y=company_trade_data_df['VWAP'], 
            mode='lines',
            name="Vwap",
            line=dict(color="#A6FF00", width=1.2)
        )
    )

    # Optional: Clean up the layout for better analysis
    fig_company.update_layout(
        title="Stock Price with 7 & 21 DMA",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=True # Often cleaner without the bottom slider
    )

    # Display in Streamlit
    st.plotly_chart(fig_company, use_container_width=True)
    
else:
    # st.error("No company selected. Please select a company from the Market Analysis page.")
    st.header(f"🏢 Search Company")
    st.text_input("Comapny")