import subprocess
import sys
import os

import streamlit as st
import pandas as pd
import numpy as np

# --- 1. Page Config & Session State Setup ---
st.set_page_config(layout="wide", page_title="Algo Screener")

if "page" not in st.session_state:
    st.session_state.page = "screener"
if "selected_stocks" not in st.session_state:
    st.session_state.selected_stocks = []

# --- 2. Data Generators ---
def get_market_data(index_name):
    # Simulate different counts based on index
    count_map = {
        "Nifty 50": 50,
        "Nifty Next 50": 50,
        "Nifty Midcap 150": 150,
        "Nifty Smallcap 250": 250
    }
    n = count_map.get(index_name, 50)
    
    # Generate Dummy Data
    np.random.seed(42) # For consistent results
    data = {
        "Select": [False] * n, # Checkbox column
        "Symbol": [f"{index_name.split()[-1].upper()}_{i}" for i in range(1, n+1)],
        "LTP": np.random.uniform(100, 3000, n).round(2),
        "Change %": np.random.uniform(-5.0, 5.0, n).round(2),
        "Volume": np.random.randint(10000, 1000000, n)
    }
    return pd.DataFrame(data)

# --- 3. Custom Styling Function ---
def color_change(val):
    """
    Custom coloring logic for individual cells (optional fallback),
    but we will use background_gradient for the whole column.
    """
    color = 'green' if val > 0 else 'red'
    return f'color: {color}'

# --- 4. Page 1: The Screener ---
def show_screener():
    st.title("🚀 Market Screener & Algo Selection")

    # A. Index Tabs
    tabs = st.tabs(["Nifty 50", "Nifty Next 50", "Nifty Midcap 150", "Nifty Smallcap 250"])
    
    selected_index = None
    active_df = None

    # Logic to handle tab content
    # We loop through tabs to render the correct data
    indices = ["Nifty 50", "Nifty Next 50", "Nifty Midcap 150", "Nifty Smallcap 250"]
    
    for i, tab in enumerate(tabs):
        with tab:
            # Load Data
            df = get_market_data(indices[i])
            
            # B. Apply Gradient Styling
            # We use Pandas Styler to create the Heatmap effect
            # cmap="RdYlGn" creates the Red -> Yellow -> Green gradient
            styled_df = df.style.background_gradient(
                subset=["Change %"], 
                cmap="RdYlGn", 
                vmin=-5, 
                vmax=5
            ).format({"LTP": "₹{:.2f}", "Change %": "{:+.2f}%"})

            # C. Display Editable Table
            st.write(f"Select stocks from **{indices[i]}** for Algo Execution:")
            
            # st.data_editor allows the user to click checkboxes
            edited_df = st.data_editor(
                styled_df,
                column_config={
                    "Select": st.column_config.CheckboxColumn(
                        "Trade?",
                        help="Select for Algo Execution",
                        default=False,
                    ),
                    "Change %": st.column_config.NumberColumn(
                        "Change %",
                        help="Daily Price Change",
                        format="%.2f %%"
                    )
                },
                disabled=["Symbol", "LTP", "Change %", "Volume"], # Only 'Select' is editable
                hide_index=True,
                use_container_width=True,
                height=500,
                key=f"editor_{indices[i]}" # Unique key for each tab
            )
            
            # Save selection logic
            if not edited_df[edited_df["Select"]].empty:
                selected_stocks = edited_df[edited_df["Select"]]["Symbol"].tolist()
                
                # Show sticky bottom container for action
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.info(f"✅ {len(selected_stocks)} stocks selected from {indices[i]}")
                    with col2:
                        if st.button(f"Proceed with {indices[i]}", key=f"btn_{i}", type="primary"):
                            st.session_state.selected_stocks = selected_stocks
                            st.session_state.source_index = indices[i]
                            st.session_state.page = "algo_setup"
                            st.rerun()

# --- 5. Page 2: Algo Setup ---
def show_algo_setup():
    st.button("← Back to Screener", on_click=lambda: st.session_state.update(page="screener"))
    
    st.title("⚡ Algo Trading Setup")
    st.success(f"Configuring Strategy for: {st.session_state.source_index}")
    
    # Display selected stocks as chips
    st.write("### Target Assets")
    st.pills("Selected Scrips", st.session_state.selected_stocks, selection_mode="multi")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Strategy", ["Momentum Breakout", "Mean Reversion", "VWAP Cross"])
        st.number_input("Capital per Trade (₹)", value=50000)
    
    with col2:
        st.selectbox("Execution Mode", ["Paper Trading", "Live Market"])
        st.slider("Stop Loss %", 0.5, 5.0, 1.0)
        
    st.button("🚀 Deploy Algo", type="primary", use_container_width=True)

# --- 6. Main Router ---
if st.session_state.page == "screener":
    show_screener()
elif st.session_state.page == "algo_setup":
    show_algo_setup()





