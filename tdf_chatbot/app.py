import requests
import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from tdf_utility.trading.nse_api import NSE_API, get_nse_india_vix, get_nse_market_status_daily

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
        ["Dashboard", "Data Analysis", "TDF ChatBot", "Settings", "About Us"]
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

elif page == "Data Analysis":
    st.subheader("Data Analysis View")

    # 1. Setup the data
    # (In a real app, you might load this from an API or file)
    duration = "1Y"
    from_dt = "30-12-2024"
    to_dt = "30-12-2025"

    nse_api = NSE_API()

    nifty_50_historical_data = nse_api._get_data(f"api/NextApi/apiClient/historicalGraph?functionName=getIndexChart&&index=NIFTY%2050&flag={duration}")

    india_vix_historical_data = get_nse_india_vix()
    india_vix_historical_data['date'] = pd.to_datetime(india_vix_historical_data['date'], format='%d-%b-%Y')

    gold_historical_data = nse_api._get_data(f"api/historical-spot-price?symbol=GOLD&fromDate={from_dt}&toDate={to_dt}")
    gold_historical_df = pd.DataFrame(gold_historical_data['data']) \
                                        .loc[:, ['UpdatedDate', 'SpotPrice2']] \
                                        .rename(columns={'UpdatedDate': 'Date', 'SpotPrice2': 'Gold 10gm'})
    gold_historical_df['Date'] = pd.to_datetime(gold_historical_df['Date'], format='%d-%b-%Y')
    gold_historical_df['Gold 10gm'] = gold_historical_df['Gold 10gm'].astype(float)

    market_status = get_nse_market_status_daily()

    # 2. Process the Data
    @st.cache_data
    def load_graph_data_to_df(object: dict):
        identifier = object.get('data').get('identifier')
        # name = objecct.get('data').get('name')
        grapth_data = object.get('data').get('grapthData')
        df = pd.DataFrame(grapth_data, columns=['Timestamp', 'Price', 'Code'])
        df['Date'] = pd.to_datetime(df['Timestamp'], unit='ms')
        return df, identifier

    nifty50_historical_graph_df, nifty50_graph_identifier = load_graph_data_to_df(nifty_50_historical_data)

    viz_df = pd.merge(nifty50_historical_graph_df.loc[:, ['Date', 'Price']].rename(columns={'Price': 'Nifty 50'}),
                  india_vix_historical_data[['date', 'close']].rename(columns={'date': 'Date', 'close': 'India VIX'}),
                  on='Date', how='left')
    viz_df = pd.merge(viz_df, gold_historical_df, on='Date', how='left')
    
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

    # Add Trace 2: India VIX (Right Axis)
    fig_nifty_gold.add_trace(
        go.Scatter(
            x=viz_df['Date'], 
            y=viz_df['Gold 10gm'], 
            name="Gold 10gm",
            line=dict(color="#F3BC0A", width=2) # Red, dotted line
        ),
        secondary_y=True, # Assign to secondary (right) axis
    )

    fig_nifty_gold.update_yaxes(title_text="<b>Nifty Price</b>", secondary_y=False)
    fig_nifty_gold.update_yaxes(title_text="<b>Gold Level</b>", secondary_y=True)

    fig_nifty_gold.update_layout(
        title=f"Nifty50 and Gold Trend",
        # xaxis_title="Date",
        yaxis_title="Nifty50",
        template="plotly_dark", # Use 'plotly_white' for light theme
        hovermode="x unified",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )


    # Render in Streamlit
    # st.markdown("### NSE Market Status")
    # st.write(market_status)
    # ₹

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
    st.plotly_chart(fig_nifty_indiavix, use_container_width=True)
    st.divider()
    st.plotly_chart(fig_nifty_gold, use_container_width=True)
    st.divider()

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