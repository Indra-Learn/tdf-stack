import streamlit as st
import pandas as pd

# Setup page
# st.set_page_config(page_title="Financial Glossary", layout="wide")


st.title("📚 Financial Knowledge Base")

# 1. Load Data & Normalize Keys
knowledgebase_dict = [
    {
        "topic": "Last Traded Price (LTP)",
        "Definition": "Represents the actual last traded price.",
        "Formula": "",
    },
    {
        "topic": "Closing Price",
        "Definition": (
            "Weighted average price of the last 30 minutes of trading."
        ),
        "Formula": "",
    },
    {"topic": "Earnings Per Share (EPS)", "Definition": "", "Formula": ""},
    {
        "topic": "P/E Ratio (Price-to-Earnings)",
        "Definition": (
            "Measures how expensive a stock is relative to its earnings by"
            " comparing share price to EPS."
        ),
        "Formula": r"\text{P/E} = \frac{\text{Current Share Price}}{\text{EPS}}",
    },
    {
        "topic": "P/B Ratio (Price-to-Book)",
        "Definition": (
            "Compares market price to book value (total assets minus"
            " intangible assets and liabilities)."
        ),
        "Formula": (
            r"\text{P/B} = \frac{\text{Market Price Per Share}}{\text{Book Value"
            r" Per Share}}"
        ),
    },
    {
        "topic": "Dividend Yield (DY)",
        "Definition": (
            "Measures the percentage of a share price paid out in annual"
            " dividends."
        ),
        "Formula": (
            r"\text{DY} = \frac{\text{Annual Dividends Per"
            r" Share}}{\text{Current Share Price}} \times 100"
        ),
    },
    {"topic": "ROE", "Definition": "", "Formula": ""},
    {"topic": "ROCE", "Definition": "", "Formula": ""},
    {
        "topic": "Ex-Date",
        "Definition": (
            "Market deadline. Shares must be purchased before this date to"
            " receive payouts."
        ),
        "Formula": "",
    },
    {
        "topic": "Record-Date",
        "Definition": (
            "Administrative date set by the board to snapshot registered"
            " shareholders."
        ),
        "Formula": "",
    },
    {
        "topic": "EQ (Equity)",
        "Definition": (
            "Standard equity series allowing both intraday and delivery trading."
        ),
        "Formula": "",
    },
    {
        "topic": "BE (Book Entry)",
        "Definition": (
            "Trade-to-Trade segment permitting only delivery-based trading."
        ),
        "Formula": "",
    },
    {
        "topic": "Free Float Market Cap (FFMC)",
        "Definition": "",
        "Formula": "",
    },
    {"topic": "Total Market Cap", "Definition": "", "Formula": ""},
]

# 2. Search & Filter Controls
col1, col2 = st.columns([3, 1])
with col1:
    search_query = st.text_input(
        "🔍 Search Topic or Keyword", ""
    ).strip().lower()
with col2:
    filter_option = st.selectbox(
        "Filter By", ["All", "With Definitions Only", "With Formulas Only"]
    )

# 3. Filter Logic
filtered_items = []
for item in knowledgebase_dict:
    topic = item.get("topic", "")
    definition = item.get("Definition", "")
    formula = item.get("Formula", "")

    # Search query filter
    matches_search = (search_query in topic.lower()) or (
        search_query in definition.lower()
    )

    # Secondary filter
    if filter_option == "With Definitions Only" and not definition:
        continue
    if filter_option == "With Formulas Only" and not formula:
        continue

    if matches_search:
        filtered_items.append(item)

# 4. Render Layout
st.caption(f"Showing {len(filtered_items)} terms")

if not filtered_items:
    st.info("No matching terms found.")

# Display in 2 responsive columns
cols = st.columns(2)
for idx, item in enumerate(filtered_items):
    col = cols[idx % 2]
    with col:
        topic = item.get("topic", "N/A")
        definition = item.get("Definition")
        formula = item.get("Formula")

        with st.expander(f"📌 **{topic}**", expanded=bool(search_query)):
            if definition:
                st.markdown(f"**Definition:** {definition}")
            else:
                st.caption("*(Definition pending)*")

            if formula:
                st.markdown("**Formula:**")
                st.latex(formula)