import requests
import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go

from tdf_utility.trading.nse_api import get_nse_market_status_daily

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
        
    st.info("Note: The sidebar scrolls independently of the main page.")


st.title("🦜🔗 TDF Applications - ")
st.markdown("---")

if page == "Dashboard":
    st.subheader("Welcome to the Dashboard")
    st.write("Here is your main content area.")

    market_status = get_nse_market_status_daily()
    st.markdown("### NSE Market Status")
    st.write(market_status)
    
    # Create simple metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Revenue", "$50,000", "+5%")
    col2.metric("Users", "1,200", "-2%")
    col3.metric("Uptime", "99.9%", "0%")

elif page == "Data Analysis":
    st.subheader("Data Analysis View")
    st.write("Placeholder for charts and dataframes.")
    st.bar_chart([10, 20, 30, 40])

    # 1. Setup the data
    # (In a real app, you might load this from an API or file)
    raw_json = {
        "data": {
            "identifier": "NIFTY 50",
            "name": "NIFTY 50",
            "grapthData": [
                [1735516800000, 23644.9, "NM"], [1735603200000, 23644.8, "NM"],
                [1735689600000, 23742.9, "NM"], [1735776000000, 24188.65, "NM"],
                [1735862400000, 24004.75, "NM"], [1736121600000, 23616.05, "NM"],
                [1736208000000, 23707.9, "NM"], [1736294400000, 23688.95, "NM"],
                [1736380800000, 23526.5, "NM"], [1736467200000, 23431.5, "NM"],
                [1736726400000, 23085.95, "NM"], [1736812800000, 23176.05, "NM"],
                [1736899200000, 23213.2, "NM"], [1736985600000, 23311.8, "NM"],
                [1737072000000, 23203.2, "NM"], [1737331200000, 23344.75, "NM"],
                [1737417600000, 23024.65, "NM"], [1737504000000, 23155.35, "NM"],
                [1737590400000, 23205.35, "NM"], [1737676800000, 23092.2, "NM"],
                [1737936000000, 22829.15, "NM"], [1738022400000, 22957.25, "NM"],
                [1738108800000, 23163.1, "NM"], [1738195200000, 23249.5, "NM"],
                [1738281600000, 23508.4, "NM"], [1738368000000, 23482.15, "NM"],
                [1738540800000, 23361.05, "NM"], [1738627200000, 23739.25, "NM"],
                [1738713600000, 23696.3, "NM"], [1738800000000, 23603.35, "NM"],
                [1738886400000, 23559.95, "NM"], [1739145600000, 23381.6, "NM"],
                [1739232000000, 23071.8, "NM"], [1739318400000, 23045.25, "NM"],
                [1739404800000, 23031.4, "NM"], [1739491200000, 22929.25, "NM"],
                [1739750400000, 22959.5, "NM"], [1739836800000, 22945.3, "NM"],
                [1739923200000, 22932.9, "NM"], [1740009600000, 22913.15, "NM"],
                [1740096000000, 22795.9, "NM"], [1740355200000, 22553.35, "NM"],
                [1740441600000, 22547.55, "NM"], [1740614400000, 22545.05, "NM"],
                [1740700800000, 22124.7, "NM"], [1740960000000, 22119.3, "NM"],
                [1741046400000, 22082.65, "NM"], [1741132800000, 22337.3, "NM"],
                [1741219200000, 22544.7, "NM"], [1741305600000, 22552.5, "NM"],
                [1741564800000, 22460.3, "NM"], [1741651200000, 22497.9, "NM"],
                [1741737600000, 22470.5, "NM"], [1741824000000, 22397.2, "NM"],
                [1742169600000, 22508.75, "NM"], [1742256000000, 22834.3, "NM"],
                [1742342400000, 22907.6, "NM"], [1742428800000, 23190.65, "NM"],
                [1742515200000, 23350.4, "NM"], [1742774400000, 23658.35, "NM"],
                [1742860800000, 23668.65, "NM"], [1742947200000, 23486.85, "NM"],
                [1743033600000, 23591.95, "NM"], [1743120000000, 23519.35, "NM"],
                [1743465600000, 23165.7, "NM"], [1743552000000, 23332.35, "NM"],
                [1743638400000, 23250.1, "NM"], [1743724800000, 22904.45, "NM"],
                [1743984000000, 22161.6, "NM"], [1744070400000, 22535.85, "NM"],
                [1744156800000, 22399.15, "NM"], [1744329600000, 22828.55, "NM"],
                [1744675200000, 23328.55, "NM"], [1744761600000, 23437.2, "NM"],
                [1744848000000, 23851.65, "NM"], [1745193600000, 24125.55, "NM"],
                [1745280000000, 24167.25, "NM"], [1745366400000, 24328.95, "NM"],
                [1745452800000, 24246.7, "NM"], [1745539200000, 24039.35, "NM"],
                [1745798400000, 24328.5, "NM"], [1745884800000, 24335.95, "NM"],
                [1745971200000, 24334.2, "NM"], [1746144000000, 24346.7, "NM"],
                [1746403200000, 24461.15, "NM"], [1746489600000, 24379.6, "NM"],
                [1746576000000, 24414.4, "NM"], [1746662400000, 24273.8, "NM"],
                [1746748800000, 24008, "NM"], [1747008000000, 24924.7, "NM"],
                [1747094400000, 24578.35, "NM"], [1747180800000, 24666.9, "NM"],
                [1747267200000, 25062.1, "NM"], [1747353600000, 25019.8, "NM"],
                [1747612800000, 24945.45, "NM"], [1747699200000, 24683.9, "NM"],
                [1747785600000, 24813.45, "NM"], [1747872000000, 24609.7, "NM"],
                [1747958400000, 24853.15, "NM"], [1748217600000, 25001.15, "NM"],
                [1748304000000, 24826.2, "NM"], [1748390400000, 24752.45, "NM"],
                [1748476800000, 24833.6, "NM"], [1748563200000, 24750.7, "NM"],
                [1748822400000, 24716.6, "NM"], [1748908800000, 24542.5, "NM"],
                [1748995200000, 24620.2, "NM"], [1749081600000, 24750.9, "NM"],
                [1749168000000, 25003.05, "NM"], [1749427200000, 25103.2, "NM"],
                [1749513600000, 25104.25, "NM"], [1749600000000, 25141.4, "NM"],
                [1749686400000, 24888.2, "NM"], [1749772800000, 24718.6, "NM"],
                [1750032000000, 24946.5, "NM"], [1750118400000, 24853.4, "NM"],
                [1750204800000, 24812.05, "NM"], [1750291200000, 24793.25, "NM"],
                [1750377600000, 25112.4, "NM"], [1750636800000, 24971.9, "NM"],
                [1750723200000, 25044.35, "NM"], [1750809600000, 25244.75, "NM"],
                [1750896000000, 25549, "NM"], [1750982400000, 25637.8, "NM"],
                [1751241600000, 25517.05, "NM"], [1751328000000, 25541.8, "NM"],
                [1751414400000, 25453.4, "NM"], [1751500800000, 25405.3, "NM"],
                [1751587200000, 25461, "NM"], [1751846400000, 25461.3, "NM"],
                [1751932800000, 25522.5, "NM"], [1752019200000, 25476.1, "NM"],
                [1752105600000, 25355.25, "NM"], [1752192000000, 25149.85, "NM"],
                [1752451200000, 25082.3, "NM"], [1752537600000, 25195.8, "NM"],
                [1752624000000, 25212.05, "NM"], [1752710400000, 25111.45, "NM"],
                [1752796800000, 24968.4, "NM"], [1753056000000, 25090.7, "NM"],
                [1753142400000, 25060.9, "NM"], [1753228800000, 25219.9, "NM"],
                [1753315200000, 25062.1, "NM"], [1753401600000, 24837, "NM"],
                [1753660800000, 24680.9, "NM"], [1753747200000, 24821.1, "NM"],
                [1753833600000, 24855.05, "NM"], [1753920000000, 24768.35, "NM"],
                [1754006400000, 24565.35, "NM"], [1754265600000, 24722.75, "NM"],
                [1754352000000, 24649.55, "NM"], [1754438400000, 24574.2, "NM"],
                [1754524800000, 24596.15, "NM"], [1754611200000, 24363.3, "NM"],
                [1754870400000, 24585.05, "NM"], [1754956800000, 24487.4, "NM"],
                [1755043200000, 24619.35, "NM"], [1755129600000, 24631.3, "NM"],
                [1755475200000, 24876.95, "NM"], [1755561600000, 24980.65, "NM"],
                [1755648000000, 25050.55, "NM"], [1755734400000, 25083.75, "NM"],
                [1755820800000, 24870.1, "NM"], [1756080000000, 24967.75, "NM"],
                [1756166400000, 24712.05, "NM"], [1756339200000, 24500.9, "NM"],
                [1756425600000, 24426.85, "NM"], [1756684800000, 24625.05, "NM"],
                [1756771200000, 24579.6, "NM"], [1756857600000, 24715.05, "NM"],
                [1756944000000, 24734.3, "NM"], [1757030400000, 24741, "NM"],
                [1757289600000, 24773.15, "NM"], [1757376000000, 24868.6, "NM"],
                [1757462400000, 24973.1, "NM"], [1757548800000, 25005.5, "NM"],
                [1757635200000, 25114, "NM"], [1757894400000, 25069.2, "NM"],
                [1757980800000, 25239.1, "NM"], [1758067200000, 25330.25, "NM"],
                [1758153600000, 25423.6, "NM"], [1758240000000, 25327.05, "NM"],
                [1758499200000, 25202.35, "NM"], [1758585600000, 25169.5, "NM"],
                [1758672000000, 25056.9, "NM"], [1758758400000, 24890.85, "NM"],
                [1758844800000, 24654.7, "NM"], [1759104000000, 24634.9, "NM"],
                [1759190400000, 24611.1, "NM"], [1759276800000, 24836.3, "NM"],
                [1759449600000, 24894.25, "NM"], [1759708800000, 25077.65, "NM"],
                [1759795200000, 25108.3, "NM"], [1759881600000, 25046.15, "NM"],
                [1759968000000, 25181.8, "NM"], [1760054400000, 25285.35, "NM"],
                [1760313600000, 25227.35, "NM"], [1760400000000, 25145.5, "NM"],
                [1760486400000, 25323.55, "NM"], [1760572800000, 25585.3, "NM"],
                [1760659200000, 25709.85, "NM"], [1760918400000, 25843.15, "NM"],
                [1761004800000, 25868.6, "NM"], [1761177600000, 25891.4, "NM"],
                [1761264000000, 25795.15, "NM"], [1761523200000, 25966.05, "NM"],
                [1761609600000, 25936.2, "NM"], [1761696000000, 26053.9, "NM"],
                [1761782400000, 25877.85, "NM"], [1761868800000, 25722.1, "NM"],
                [1762128000000, 25763.35, "NM"], [1762214400000, 25597.65, "NM"],
                [1762387200000, 25509.7, "NM"], [1762473600000, 25492.3, "NM"],
                [1762732800000, 25574.35, "NM"], [1762819200000, 25694.95, "NM"],
                [1762905600000, 25875.8, "NM"], [1762992000000, 25879.15, "NM"],
                [1763078400000, 25910.05, "NM"], [1763337600000, 26013.45, "NM"],
                [1763424000000, 25910.05, "NM"], [1763510400000, 26052.65, "NM"],
                [1763596800000, 26192.15, "NM"], [1763683200000, 26068.15, "NM"],
                [1763942400000, 25959.5, "NM"], [1764028800000, 25884.8, "NM"],
                [1764115200000, 26205.3, "NM"], [1764201600000, 26215.55, "NM"],
                [1764288000000, 26202.95, "NM"], [1764547200000, 26175.75, "NM"],
                [1764633600000, 26032.2, "NM"], [1764720000000, 25986, "NM"],
                [1764806400000, 26033.75, "NM"], [1764892800000, 26186.45, "NM"],
                [1765152000000, 25960.55, "NM"], [1765238400000, 25839.65, "NM"],
                [1765324800000, 25758, "NM"], [1765411200000, 25898.55, "NM"],
                [1765497600000, 26046.95, "NM"], [1765756800000, 26027.3, "NM"],
                [1765843200000, 25860.1, "NM"], [1765929600000, 25818.55, "NM"],
                [1766016000000, 25815.55, "NM"], [1766102400000, 25966.4, "NM"],
                [1766361600000, 26172.4, "NM"], [1766448000000, 26177.15, "NM"],
                [1766534400000, 26142.1, "NM"], [1766707200000, 26042.3, "NM"],
                [1766966400000, 25942.1, "NM"]
            ],
            "closePrice": 0
        }
    }

    # 2. Process the Data
    @st.cache_data
    def load_data(json_data):
        graph_data = json_data['data']['grapthData']
        identifier = json_data['data']['identifier']
        
        # Create DataFrame
        # Column 0: Timestamp (ms), Column 1: Price, Column 2: Flag/Code
        df = pd.DataFrame(graph_data, columns=['Timestamp', 'Price', 'Code'])
        
        # Convert Timestamp (ms) to proper DateTime objects
        df['Date'] = pd.to_datetime(df['Timestamp'], unit='ms')
        
        return df, identifier

    df, identifier = load_data(raw_json)

    # 3. Streamlit Layout
    st.markdown("Historical price movement visualization.")

    # 4. Create Interactive Plot with Plotly
    # Interactive allows zooming, hovering to see exact price/date
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Price'],
        mode='lines',
        name=identifier,
        line=dict(color='#00C805', width=2), # Green stock line color
        hovertemplate='<b>Date</b>: %{x|%d %b %Y}<br><b>Price</b>: %{y:.2f}<extra></extra>'
    ))

    # Styling the layout
    fig.update_layout(
        title=f"{identifier} Price Trend",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_dark", # Use 'plotly_white' for light theme
        hovermode="x unified"
    )

    # Render in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # 5. Show Raw Data (Optional)
    with st.expander("View Raw Data"):
        st.dataframe(df[['Date', 'Price']].style.format({"Price": "{:.2f}"}))

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
