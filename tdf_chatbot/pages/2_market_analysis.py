import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from src.market_data_fetcher import sourcing_viz_data, sourcing_nifty_index_data
from src.streamlit_styles import style_metric_cards
from src.streamlit_side_navbar import render_sidebar

st.set_page_config(page_title="Market Analysis", layout="wide")

render_sidebar()
style_metric_cards()

if "viz_df" not in st.session_state:
    st.session_state["viz_df"] = None
if "nifty_heatmap_df" not in st.session_state:
    st.session_state["nifty_heatmap_df"] = None


st.subheader("TheDataFestAI - Market Analysis")
st.write("Investment is subject to market risk. Please read all scheme related documents carefully before investing.")
st.write("Also do you your own thorough research carefully before investing.")
st.markdown("---")

# 1. Setup the data and 2. Process the Data
# (In a real app, you might load this from an API or file)

if st.session_state["viz_df"] is None:
    with st.spinner("Fetching data for analysing with visualizations..."):
        # This block runs ONLY once per session
        viz_df = sourcing_viz_data()
        st.session_state["viz_df"] = viz_df
        st.sidebar.success("API Called Successfully First Time. Data Cached for viz.")
viz_df = st.session_state["viz_df"]

if st.session_state["nifty_heatmap_df"] is None:
    with st.spinner("Fetching data for nifty index with visualizations..."):
        nifty_heatmap_df = sourcing_nifty_index_data()
        st.session_state["nifty_heatmap_df"] = nifty_heatmap_df
        st.sidebar.success("API Called Successfully First Time. Data Cached for nifty index.")
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
silver_1kg_diff = (latest_data["Silver 1kg"] - prev_data["Silver 1kg"]) / prev_data["Silver 1kg"] * 100
crude_oil_diff = (latest_data["Crude Oil"] - prev_data["Crude Oil"]) / prev_data["Crude Oil"] * 100

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Nifty 50", f"₹{latest_data['Nifty 50']:.2f}", f"{nifty50_diff:.2f}%")
col2.metric("India VIX", f"{latest_data['India VIX']:.2f}", f"{india_vix_diff:.2f}%", delta_color="inverse")
col3.metric("Gold 10gm", f"₹{latest_data['Gold 10gm']:.2f}", f"{gold_10gm_diff:.2f}%")
col4.metric("Silver 1kg", f"₹{latest_data['Silver 1kg']:.2f}", f"{silver_1kg_diff:.2f}%")
col5.metric("Crude Oil", f"₹{latest_data['Crude Oil']:.2f}", f"{crude_oil_diff:.2f}%")

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

        df = df.loc[:, ['symbol', 'lastPrice', 'pchange', 'high', 'low', 'tradedVolume', 'tradedValue', 'vwap', 'Research', 'Company Profile']]
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
                "Company Profile": st.column_config.LinkColumn(
                    "Company Profile",
                    validate="^https://.+$",
                    display_text="Get Details",
                    help="Click to view detailed report",
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