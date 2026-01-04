import requests
import streamlit as st
import pandas as pd
import json
from time import sleep
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from tdf_utility.trading.nse_api import NSE_API, get_nse_india_vix, get_nse_market_status_daily, get_nifty_heatmap
from tdf_utility.trading.ep_api import fetch_fii_dii_data

# configure
tdf_api_url = "72.61.231.147:8000"

def call_tdf_llm_apis(endpoint: str, company_ticker: str) -> str:
    """
    Docstring for call_tdf_llm_apis
    
    :param endpoint: Description
    :type endpoint: str
    :param company_ticker: Description
    :type company_ticker: str
    :return: Description
    :rtype: str

    1. http://72.61.231.147:8000/company_summary
    2. http://72.61.231.147:8000/sector_summary
    3. http://72.61.231.147:8000/investment_recommendations
    """
    response = requests.post(f"http://{tdf_api_url}/{endpoint}/invoke",
                             json={"input": {"company_ticker": company_ticker}})
    if response.status_code == 200:
        return response.json().get("output").get("content", 
                                                 "No data available for endpoint: {endpoint} and company: {company_ticker}.")
    else:
        return f"Error: {response.status_code} - {response.text}"


@st.cache_data
def load_graph_data_to_df(object: dict):
    identifier = object.get('data').get('identifier')
    # name = objecct.get('data').get('name')
    grapth_data = object.get('data').get('grapthData')
    df = pd.DataFrame(grapth_data, columns=['Timestamp', 'Price', 'Code'])
    df['Date'] = pd.to_datetime(df['Timestamp'], unit='ms')
    return df, identifier

def sourcing_viz_data():
        duration = "1Y"
        year = "2025"
        from_dt = "31-12-2024"
        to_dt = "30-12-2025"

        nse_api = NSE_API()
        
        nifty_50_historical_data = nse_api._get_data(f"api/NextApi/apiClient/historicalGraph?functionName=getIndexChart&&index=NIFTY%2050&flag={duration}")

        india_vix_historical_data = get_nse_india_vix()
        india_vix_historical_data['date'] = pd.to_datetime(india_vix_historical_data['date'], format='%d-%b-%Y')

        sleep(2)
        gold_historical_data = nse_api._get_data(f"api/historical-spot-price?symbol=GOLD&fromDate={from_dt}&toDate={to_dt}")
        gold_historical_df = pd.DataFrame(gold_historical_data['data']) \
                                            .loc[:, ['UpdatedDate', 'SpotPrice2']] \
                                            .rename(columns={'UpdatedDate': 'Date', 'SpotPrice2': 'Gold 10gm'})
        gold_historical_df['Date'] = pd.to_datetime(gold_historical_df['Date'], format='%d-%b-%Y')
        gold_historical_df['Gold 10gm'] = gold_historical_df['Gold 10gm'].astype(float)

        sleep(2)
        silver_historical_data = nse_api._get_data(f"api/historical-spot-price?symbol=SILVER&fromDate={from_dt}&toDate={to_dt}")
        silver_historical_df = pd.DataFrame(silver_historical_data['data']) \
                                            .loc[:, ['UpdatedDate', 'SpotPrice2']] \
                                            .rename(columns={'UpdatedDate': 'Date', 'SpotPrice2': 'Silver 1kg'})
        silver_historical_df['Date'] = pd.to_datetime(silver_historical_df['Date'], format='%d-%b-%Y')
        silver_historical_df['Silver 1kg'] = silver_historical_df['Silver 1kg'].astype(float)

        crudeoil_historical_data = nse_api._get_data(f"api/historical-spot-price?symbol=CRUDEOIL&fromDate={from_dt}&toDate={to_dt}")
        crudeoil_historical_df = pd.DataFrame(crudeoil_historical_data['data']) \
                                            .loc[:, ['UpdatedDate', 'SpotPrice1']] \
                                            .rename(columns={'UpdatedDate': 'Date', 'SpotPrice1': 'Crude Oil'})
        crudeoil_historical_df['Date'] = pd.to_datetime(crudeoil_historical_df['Date'], format='%d-%b-%Y')
        crudeoil_historical_df['Crude Oil'] = crudeoil_historical_df['Crude Oil'].astype(float)

        fii_dii_data_df = fetch_fii_dii_data(year=year)

        nifty50_historical_graph_df, nifty50_graph_identifier = load_graph_data_to_df(nifty_50_historical_data)

        viz_df = pd.merge(nifty50_historical_graph_df.loc[:, ['Date', 'Price']].rename(columns={'Price': 'Nifty 50'}),
                    india_vix_historical_data[['date', 'close']].rename(columns={'date': 'Date', 'close': 'India VIX'}),
                    on='Date', how='left')
        viz_df = pd.merge(viz_df, gold_historical_df, on='Date', how='left')
        viz_df = pd.merge(viz_df, silver_historical_df, on='Date', how='left')
        viz_df = pd.merge(viz_df, crudeoil_historical_df, on='Date', how='left')
        viz_df = pd.merge(viz_df, fii_dii_data_df, on='Date', how='left')

        # market_status = get_nse_market_status_daily()

        return viz_df

def sourcing_nifty_index_data():
    nse_api = NSE_API()
    nifty_heatmap_df = get_nifty_heatmap()
    return nifty_heatmap_df

## Streamlit App
def style_metric_cards(background_color="#1E1E1E", border_color="#333333"):
    st.markdown(f"""
    <style>
    /* Target the container for st.metric */
    [data-testid="stMetric"] {{
        background-color: {background_color};
        border: 1px solid {border_color};
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        /* Center content if desired */
        text-align: center; 
    }}

    /* Optional: Style the label (e.g., "Nifty 50") */
    [data-testid="stMetricLabel"] {{
        font-weight: bold;
        color: #aaaaaa; /* Light grey text */
    }}
    
    /* Optional: Style the delta arrow */
    [data-testid="stMetricDelta"] svg {{
        /* You can adjust size here if needed */
    }}
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(
    page_title="TDF Streamlit App",
    layout="wide",  # Use 'wide' layout to maximize screen space
    initial_sidebar_state="expanded"
)

with st.sidebar:
    st.header("📲 Navigator")
    
    # Simulating a Navigation Menu using radio buttons
    page = st.radio(
        "Go to",
        ["Dashboard", "Market Analysis", "TDF ChatBot", "Settings", "About Us"]
    )
    
    st.divider() # Adds a visual line separator

    nifty_dashboard_page = st.selectbox(
        "Nifty Dashboard Pages",
        ["Nifty 50", "Nifty Bank"]
    )
    
    st.divider()

    st.info("Note: The sidebar scrolls independently of the main page.")


style_metric_cards()
st.title("🦜🔗 TDF Applications - ")
st.markdown("---")

if "viz_df" not in st.session_state:
    st.session_state["viz_df"] = None
if "nifty_heatmap_df" not in st.session_state:
    st.session_state["nifty_heatmap_df"] = None

if page == "Dashboard":
    st.subheader("Welcome to the Dashboard")
    st.write("Here is your main content area.")
    
    # Create simple metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Revenue", "$50,000", "+5%")
    col2.metric("Users", "1,200", "-2%")
    col3.metric("Uptime", "99.9%", "0%")

    # 1. Setup Dummy Data (Matching your previous structure)
    data = {
        "Date": ["2025-12-29", "2025-12-30"],
        "Nifty 50": [25942.10, 25938.85],  # Price dropped slightly
        "India VIX": [9.72, 9.68]          # Volatility dropped slightly
    }
    df = pd.DataFrame(data)

    # 2. Calculation Logic
    # Get the latest data (Last row)
    latest_data = df.iloc[-1]
    # Get the previous data (Second to last row)
    prev_data = df.iloc[-2]

    # Calculate Changes (Deltas)
    nifty_change = latest_data["Nifty 50"] - prev_data["Nifty 50"]
    vix_change = latest_data["India VIX"] - prev_data["India VIX"]

    # 3. Create Columns
    col1, col2 = st.columns(2)

    # 4. Render Metrics
    # f"{value:.2f}" formats the number to 2 decimal places

    with col1:
        st.metric(
            label="Nifty 50",
            value=f"{latest_data['Nifty 50']:.2f}",
            delta=f"{nifty_change:.2f}"
        )

    with col2:
        st.metric(
            label="India VIX",
            value=f"{latest_data['India VIX']:.2f}",
            delta=f"{vix_change:.2f}",
            delta_color="inverse" 
        )

elif page == "Market Analysis":
    st.subheader("TDF - Market Analysis")

    # 1. Setup the data and 2. Process the Data
    # (In a real app, you might load this from an API or file)
    
    if st.session_state["viz_df"] is None:
        with st.spinner("Fetching data for analysing with visualizations..."):
            # This block runs ONLY once per session
            viz_df = sourcing_viz_data()
            st.session_state["viz_df"] = viz_df
            st.success("API Called Successfully First Time. Data Cached for viz.")
    viz_df = st.session_state["viz_df"]

    if st.session_state["nifty_heatmap_df"] is None:
        with st.spinner("Fetching data for nifty index with visualizations..."):
            nifty_heatmap_df = sourcing_nifty_index_data()
            st.session_state["nifty_heatmap_df"] = nifty_heatmap_df
            st.success("API Called Successfully First Time. Data Cached for nifty index.")
    nifty_heatmap_df = st.session_state["nifty_heatmap_df"]

    # 3. Streamlit Layout
    st.markdown("Historical price movement visualization.")

    # 4. Create Interactive Plot with Plotly
    # Interactive allows zooming, hovering to see exact price/date
    fig_nifty_indiavix = make_subplots(specs=[[{"secondary_y": True}]])

    # Add Trace 1: Nifty 50 (Left Axis)
    fig_nifty_indiavix.add_trace(
        go.Scatter(
            x=viz_df['Date'], 
            y=viz_df['Nifty 50'], 
            name="Nifty 50",
            line=dict(color='#00C805', width=2)
        ),
        secondary_y=False, # Assign to primary (left) axis
    )

    # Add Trace 2: India VIX (Right Axis)
    fig_nifty_indiavix.add_trace(
        go.Scatter(
            x=viz_df['Date'], 
            y=viz_df['India VIX'], 
            name="India VIX",
            line=dict(color='#FF5733', width=2) # Red, dotted line
        ),
        secondary_y=True, # Assign to secondary (right) axis
    )

    fig_nifty_indiavix.update_yaxes(title_text="<b>Nifty Price</b>", secondary_y=False)
    fig_nifty_indiavix.update_yaxes(title_text="<b>VIX Level</b>", secondary_y=True)

    fig_nifty_indiavix.update_layout(
        title=f"Nifty50 and India VIX Trend",
        # xaxis_title="Date",
        yaxis_title="Nifty50",
        template="plotly_dark", # Use 'plotly_white' for light theme
        hovermode="x unified",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    
    # Another Fig
    fig_nifty_gold = make_subplots(specs=[[{"secondary_y": True}]])

    # Add Trace 1: Nifty 50 (Left Axis)
    fig_nifty_gold.add_trace(
        go.Scatter(
            x=viz_df['Date'], 
            y=viz_df['Nifty 50'], 
            name="Nifty 50",
            line=dict(color='#00C805', width=2)
        ),
        secondary_y=False, # Assign to primary (left) axis
    )
    # Add Trace 2: Gold 10gm (Right Axis)
    fig_nifty_gold.add_trace(
        go.Scatter(
            x=viz_df['Date'], 
            y=viz_df['Gold 10gm'], 
            name="Gold 10gm",
            line=dict(color="#F3BC0A", width=2) # Red, dotted line
        ),
        secondary_y=True, # Assign to secondary (right) axis
    )
    # Add Trace 3: Silver 1kg (Right Axis)
    fig_nifty_gold.add_trace(
        go.Scatter(
            x=viz_df['Date'], 
            y=viz_df['Silver 1kg'], 
            name="Silver 1kg",
            line=dict(color="#9BAAC3", width=2)
        ),
        secondary_y=True, # Assign to secondary (right) axis
    )

    fig_nifty_gold.update_yaxes(title_text="<b>Nifty Price</b>", secondary_y=False)
    fig_nifty_gold.update_yaxes(title_text="<b>Gold & Silver Level</b>", secondary_y=True)

    fig_nifty_gold.update_layout(
        title=f"Nifty50 and Gold Trend",
        # xaxis_title="Date",
        yaxis_title="Nifty50",
        template="plotly_dark", # Use 'plotly_white' for light theme
        hovermode="x unified",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )

    # another fig
    fig_nifty_fii_dii = make_subplots(specs=[[{"secondary_y": True}]])

    # Trace 1: FII Net (Blue Bars)
    fig_nifty_fii_dii.add_trace(
        go.Bar(
            x=viz_df['Date'],
            y=viz_df['FII Net'],
            name="FII Net",
            marker_color="#0026FF", # Light Blue
            # opacity=0.8
        ),
        secondary_y=False, # Left Axis
    )

    # Trace 2: DII Net (Red Bars)
    fig_nifty_fii_dii.add_trace(
        go.Bar(
            x=viz_df['Date'],
            y=viz_df['DII Net'],
            name="DII Net",
            marker_color="#9D00FF", # Red/Pink
            # opacity=0.8
        ),
        secondary_y=False, # Left Axis
    )

    # Trace 3: Nifty 50 (Black Line) - Added LAST so it appears ON TOP
    fig_nifty_fii_dii.add_trace(
        go.Scatter(
            x=viz_df['Date'],
            y=viz_df['Nifty 50'],
            name="Nifty 50",
            mode='lines+markers',
            line=dict(color="#00C805", width=3), # Dark line for contrast
            marker=dict(size=4)
        ),
        secondary_y=True, # Right Axis
    )

    # --- 3. Layout Customization ---
    fig_nifty_fii_dii.update_layout(
        title="Institutional Flows vs Market Direction",
        barmode='group', # Puts FII and DII bars side-by-side
        height=600,
        hovermode="x unified", # Shows all 3 values when hovering over a date
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_white"
    )

    # Axis Titles
    fig_nifty_fii_dii.update_yaxes(title_text="<b>Net Flow (₹ Cr)</b>", secondary_y=False)
    fig_nifty_fii_dii.update_yaxes(title_text="<b>Nifty 50 Price</b>", secondary_y=True, showgrid=False)

    fig_crudeoil = px.bar(viz_df, x='Date', y='Crude Oil', title='Crude Oil Prices Over Time', template='plotly_dark')

    # Render in Streamlit
    # st.markdown("### NSE Market Status")
    # st.write(market_status)

    # Create simple metrics
    latest_data = viz_df.iloc[-1]
    prev_data = viz_df.iloc[-2]
    nifty50_diff = (latest_data["Nifty 50"] - prev_data["Nifty 50"]) / prev_data["Nifty 50"] * 100
    india_vix_diff = (latest_data["India VIX"] - prev_data["India VIX"]) / prev_data["India VIX"] * 100
    gold_10gm_diff = (latest_data["Gold 10gm"] - prev_data["Gold 10gm"]) / prev_data["Gold 10gm"] * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Nifty 50", f"₹{latest_data['Nifty 50']:.2f}", f"{nifty50_diff:.2f}%")
    col2.metric("India VIX", f"{latest_data['India VIX']:.2f}", f"{india_vix_diff:.2f}%", delta_color="inverse")
    col3.metric("Gold 10gm", f"₹{latest_data['Gold 10gm']:.2f}", f"{gold_10gm_diff:.2f}%")

    st.divider()
    st.markdown("### [Nifty 50 Trends](https://www.nseindia.com/index-tracker/NIFTY%2050)")
    st.plotly_chart(fig_nifty_indiavix, use_container_width=True)
    st.divider()
    st.plotly_chart(fig_nifty_fii_dii, use_container_width=True)
    st.divider()
    st.markdown("### [Nifty Commodities Spot Price](https://www.nseindia.com/historical-spot-price)")
    st.plotly_chart(fig_nifty_gold, use_container_width=True)
    st.plotly_chart(fig_crudeoil, use_container_width=True)
    st.divider()

    # "Nifty Next 50", "Nifty Midcap 150", "Nifty Smallcap 250", "Others"
    indices = ["Nifty 50", "Nifty Next 50"]
    tabs = st.tabs(indices)
    for i, tab in enumerate(tabs):
        with tab:
            st.markdown(f"### 🚀 {indices[i]} Heatmap")

            # Load Data
            if indices[i] == "Nifty 50":
                df = nifty_heatmap_df[nifty_heatmap_df["nse_index"]=="Nifty 50"]
            elif indices[i] == "Nifty Next 50":
                df = nifty_heatmap_df[nifty_heatmap_df["nse_index"]=="Nifty Next 50"]
            else:
                df = pd.DataFrame()

            df = df.loc[:, ['symbol', 'lastPrice', 'pchange', 'high', 'low', 'tradedVolume', 'tradedValue', 'vwap', 'Research']]
            df.rename(columns={'symbol': 'Symbol', 
                                'lastPrice': 'Last Price', 
                                'pchange': 'Change %', 
                                'high': 'High', 
                                'low': 'Low', 
                                'tradedVolume': 'Volume', 
                                'tradedValue': 'Value', 
                                'vwap': 'VWAP'}, inplace=True)
            df['Select'] = False
            styled_df = df.style.background_gradient(
                subset=["Change %"], 
                cmap="RdYlGn", 
                vmin=-2, 
                vmax=2
            ).format({"Last Price": "₹{:.2f}", "Change %": "{:+.2f}%", "High": "₹{:.2f}", "Low": "₹{:.2f}", "Value": "₹{:.2f}", "VWAP": "₹{:.2f}"})

            edited_df = st.data_editor(
                styled_df,
                column_config={
                    "Research": st.column_config.LinkColumn(
                        "Research",
                        validate="^https://.+$",
                        display_text="Click Here",
                        help="Click to view detailed research report",
                    ),
                    "Select": st.column_config.CheckboxColumn(
                        "Trade?",
                        help="Select for Algo Execution",
                        default=False,
                    ),
                    "Change %": st.column_config.NumberColumn(
                        "Change %",
                        help="Daily Price Change",
                        format="%.2f %%"
                    ),
                    "Volume": st.column_config.NumberColumn(
                        "Volume(Lakhs)",
                        help="Number of shares or contracts exchanged"
                    ),
                    "Value": st.column_config.NumberColumn(
                        "Value(Cr.)",
                        help="Turnover = Price x Volume"
                    ),
                    "VWAP": st.column_config.NumberColumn(
                        "VWAP",
                        help="Volume Weighted Average Price = Value / Volume"
                    )
                },
                # symbol	lastPrice	pchange	high	low	tradedVolume	tradedValue	vwap
                disabled=["Symbol", "Last Price", "Change %", "High", "Low", "Volume", "Value", "VWAP"],
                hide_index=True,
                use_container_width=True,
                height=500,
                key=f"editor_{indices[i]}" # Unique key for each tab
            )


    st.divider()
    st.markdown("**Disclaimer:** This is for information purposes only. These are not stock recommendations and should not be treated as such. Learn more about our recommendation services here... Also note that these screeners are based only on numbers. There is no screening for management quality.")


    

    # 5. Show Raw Data (Optional)
    # with st.expander("View Raw Data"):
    #     st.dataframe(df[['Date', 'Price']].style.format({"Price": "{:.2f}"}))

elif page == "TDF ChatBot":
    st.subheader("TDF ChatBot Interface")
    st.write("Interact with the TDF ChatBot here.")
    st.html("<h3>🚀 Get company and sector summaries using TDF API.</h3>")
    input_company_ticker = st.text_input("Enter Company Ticker (e.g., Reliance, HDFC, SBI):")

    if input_company_ticker:
        company_summary = call_tdf_llm_apis("company_summary", input_company_ticker)
        st.subheader("Company Summary")
        st.write(company_summary)

        sector_summary = call_tdf_llm_apis("sector_summary", input_company_ticker)
        st.subheader("Sector Summary")
        st.write(sector_summary)

        investment_summary = call_tdf_llm_apis("investment_recommendations", input_company_ticker)
        st.subheader("Investment Recommendations")
        st.write(investment_summary)

    # if input_company_ticker:
    #     if st.button("Get Company Summary"):
    #         company_summary = get_company_summary(input_company_ticker)
    #         st.subheader("Company Summary")
    #         st.write(company_summary)
            
    #     if st.button("Get Sector Summary"):
    #         sector_summary = get_sector_summary(input_company_ticker)
    #         st.subheader("Sector Summary")
    #         st.write(sector_summary)

elif page == "Settings":
    st.subheader("User Settings")
    st.checkbox("Enable Dark Mode")
    st.checkbox("Show Notifications")

elif page == "About Us":
    st.subheader("About This App")
    st.write("This application was built to demonstrate a simple navbar layout.")

elif nifty_dashboard_page == "Nifty 50":
    st.subheader("Nifty 50 Dashboard")
    st.markdown("Details and analytics for [Nifty 50](https://www.nseindia.com/index-tracker/NIFTY%2050).")