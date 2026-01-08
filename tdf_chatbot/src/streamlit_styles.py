import streamlit as st

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