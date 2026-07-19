import streamlit as st
import pandas as pd

st.header("ETF Analysis")



# 1. Your Dynamic Data Source
screener_dict = {
    "FII Buying": "https://www.screener.in/screens/343087/fii-buying/",
    "PAT > 0 in qtr": "https://www.screener.in/screens/608536/all-latest-quarterly-results/",
    "Debt Free": "https://www.screener.in/screens/1/debt-free/",
    "High ROE": "https://www.screener.in/screens/2/high-roe/",
    "Value Stocks": "https://www.screener.in/screens/3/value-stocks/",
    # Add as many as you want; the grid will auto-wrap every 8 items
}

# 2. State Initialization
if "active_screen_name" not in st.session_state:
    st.session_state.active_screen_name = None
if "screen_data" not in st.session_state:
    st.session_state.screen_data = pd.DataFrame()

# 3. The Callback Function
# This runs instantly when a button is clicked, BEFORE the rest of the script reruns
def handle_button_click(name: str, url: str):
    st.session_state.active_screen_name = name
    
    # ⚠️ Replace this dummy dataframe with your actual async fetch_screener_data(url) function
    st.session_state.screen_data = pd.DataFrame({
        "Screen": [name],
        "URL": [url],
        "Status": ["Data Fetched Successfully"]
    })

st.title("⚡ Dynamic Algo Screens")

# 4. The Grid Generator Engine
BUTTONS_PER_ROW = 8
items = list(screener_dict.items())

# Loop through the list in chunks of 8
for i in range(0, len(items), BUTTONS_PER_ROW):
    # Slice exactly 8 items (or fewer if at the end of the list)
    chunk = items[i : i + BUTTONS_PER_ROW]
    
    # Create 8 fixed columns for the row
    cols = st.columns(BUTTONS_PER_ROW)
    
    # Zip the columns and the chunk together to place one button per column
    for col, (name, url) in zip(cols, chunk):
        with col:
            # ⚠️ Unique 'key' is mandatory when generating buttons in a loop
            st.button(
                label=name,
                key=f"btn_{name}",
                on_click=handle_button_click,
                args=(name, url), # Passes these variables into the callback function
                width='stretch' # Stretches the button to fill the column cleanly
            )

st.divider()

# 5. Render the result
if st.session_state.active_screen_name:
    st.subheader(f"📊 Results for: {st.session_state.active_screen_name}")
    st.dataframe(st.session_state.screen_data, width='stretch', hide_index=True)
else:
    st.info("Select a screen from the grid above to fetch data.")