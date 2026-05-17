import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from streamlit_extras.card_selector import card_selector
from streamlit_extras.steps import steps
from streamlit_extras.stodo import to_do
from utilities.mutualfund import mf_data
from utilities import calculations as calc

# st.header(":rainbow[Mutual Fund - Sahi Hai! or Not?]", divider=True)
# st.markdown(
#     """
#     Mutual funds are a popular investment vehicle that pool money from multiple investors to invest in a diversified portfolio of stocks, bonds, or other securities. They offer several advantages, such as professional management, diversification, and liquidity. However, like any investment, mutual funds also have their drawbacks and risks. 

#     **Advantages of Mutual Funds:**
#     1. **Professional Management:** Mutual funds are managed by experienced fund managers who make investment decisions on behalf of the investors.
#     2. **Diversification:** By investing in a mutual fund, investors can gain exposure to a wide range of securities, which helps to spread risk.
#     3. **Liquidity:** Mutual funds can be bought or sold on any business day at the current net asset value (NAV), providing investors with easy access to their money.

#     **Disadvantages of Mutual Funds:**
#     1. **Fees and Expenses:** Mutual funds charge management fees and other expenses that can eat into returns over time.
#     2. **Lack of Control:** Investors do not have control over the specific securities in the fund's portfolio, which may not align with their individual preferences or risk tolerance.
#     3. **Market Risk:** Like all investments, mutual funds are subject to market risk, and there is no guarantee of returns.

#     In conclusion, whether mutual funds are "sahi hai" (good) or not depends on individual financial goals, risk tolerance, and investment preferences. It's important for investors to carefully research and consider these factors before investing in mutual funds.
#     """
# )

st.subheader(":rainbow[Step 1:  Why To Invest?]", divider="violet")
why_to_invest_cards = mf_data.get_mf_info().get("why_to_invest", [])
selected = card_selector(
        [dict(icon=i["icon"], title=i["title"], description=i["description"]) for i in why_to_invest_cards],
        selection_mode="multi",
        key="demo_multi",
    )
if selected:
    st.write(f"Selected: **{[why_to_invest_cards[i]['title'] for i in selected]}**")
st.markdown("""
    In summary, investing is a powerful tool for building wealth, achieving financial goals, and securing your financial future. It's important to start early, diversify your investments, and stay informed to make the most of your investment journey.
""")

# st.subheader(":rainbow[Step 2:  Define Goal:]", divider="violet")

def factors_to_evaluate_investments() -> None:
    factors_to_consider = mf_data.get_mf_info().get("factors_to_consider", [])
    title = [factor["title"] for factor in factors_to_consider]
    icons=[factor["icon"] for factor in factors_to_consider]
    description = [factor["description"] for factor in factors_to_consider]

    h_steps = steps(
        title,
        horizontal=True,
        icons=icons,
        key="demo_hd",
    )
    
    for i, factor in enumerate(factors_to_consider):
        with h_steps[i]:
            st.markdown(f"#### {factor['icon']} {factor['title']}")
            st.markdown(factor["description"])
            if i == 0:
                if st.button("Next", icon="⏩", key=f"hd_next_{i}"):
                    h_steps.next()
            elif i < len(factors_to_consider) - 1:
                col1, col2, col3 = st.columns([1, 1, 10])
                with col1:
                    if st.button("Back", icon="⏪", key=f"hd_back_{i}"):
                        h_steps.previous()
                with col2:
                    if st.button("Next", icon="⏩", key=f"hd_next_{i}"):
                        h_steps.next()
            else:
                col1, col2, col3 = st.columns([1, 1, 10])
                with col1:
                    if st.button("Back", icon="⏪", key=f"hd_back_{i}"):
                        h_steps.previous()
                with col2:
                    if st.button("Reset", icon="🔄", key="hd_reset"):
                        h_steps.reset()

st.subheader(":rainbow[Step 2:  Factors to Evaluate Investments:]", divider="violet")
factors_to_evaluate_investments()


st.subheader(":rainbow[Step 3:  Different Asset Classes:]", divider="violet")
different_asset_classes = mf_data.get_mf_info().get("different_asset_classes", [])

selected_asset_class = card_selector(
    [dict(icon="📘", title=i["product"]) for i in different_asset_classes],
    selection_mode="single",
    key="demo_single",
)

if selected_asset_class is not None:
    st.write(f"Selected: **{different_asset_classes[selected_asset_class]['product']}**")
    for detail in different_asset_classes[selected_asset_class]['details']:
        # st.markdown(f"- {detail['instrument']}")
        st.markdown(f"""
            <div style="border-left: 3px solid #185FA5; padding: 4px 12px; 
                        margin-bottom: 6px; font-size: 14px;">
                {detail['instrument']}
            </div>
            """, unsafe_allow_html=True)

# MAX_COLS = 3
# for i in range(0, len(different_asset_classes), MAX_COLS):
#     chunk = different_asset_classes[i : i + MAX_COLS]
#     cols = st.columns(MAX_COLS)
#     for j, item in enumerate(chunk):
#         with cols[j].container(height=225, gap="small"):
#             st.markdown(f"### 📘 {item['product']}")
#             if "details" in item:
#                 for detail in item['details']:
#                     st.markdown(f"- {detail['instrument']}")

st.subheader(":rainbow[Step 4:  Compound Interest Calculator]", divider="violet")
col1, col2 = st.columns([1, 3], border=True)

with col1:
    principal = st.slider("Initial Principal (₹)", min_value=1000, max_value=100000, value=10000, step=500, format="₹%d")
    interest_rate = st.slider("Annual Interest Rate (%)", min_value=1.0, max_value=50.0, value=12.0, step=0.5, format="%.1f%%")
    years = st.slider("Time Period (Years)", min_value=1, max_value=40, value=5, step=1)
    freq_label = st.selectbox("Compounding Frequency", options=["Yearly", "Quarterly", "Monthly", "Daily"], index=0)

    freq_map = {"Yearly": 1, "Quarterly": 4, "Monthly": 12, "Daily": 365}
    n = freq_map[freq_label]
    r = interest_rate / 100

    final_balance = calc.compound(principal, r, n, years)
    total_interest = final_balance - principal
    simple_interest_total = principal + principal * r * years

with col2:
    # col1, col2, col3 = st.columns(3)
    # with col1:
    #     st.metric("Final Balance", f"₹{final_balance:,.0f}")
    # with col2:
    #     st.metric("Total Interest Earned (Compound)", f"₹{total_interest:,.0f}",
    #             delta=f"+{(total_interest/principal*100):.1f}% return")
    # with col3:
    #     st.metric(
    #         "vs Simple Interest",
    #         f"+₹{final_balance - simple_interest_total:,.0f}"
    #     )
    year_range = list(range(0, years + 1))
    balances = [calc.compound(principal, r, n, t) for t in year_range]
    principals = [principal] * len(year_range)
    interests = [b - principal for b in balances]
    
    df = pd.DataFrame({
        "Year": year_range,
        "Total Balance": [round(b, 2) for b in balances],
        "Principal": [round(p, 2) for p in principals],
        "Interest Earned": [round(i, 2) for i in interests],
        "Simple Interest Balance": [round(principal + principal * r * t, 2) for t in year_range]
    })

    fig = go.Figure()

    fig.add_trace(go.Bar(x=df["Year"], y=df["Principal"], name="Principal", marker_color="#888780"))
    fig.add_trace(go.Bar(x=df["Year"], y=df["Interest Earned"], name="Interest Earned", marker_color="#1D9E75"))
    fig.add_trace(go.Scatter(
        x=df["Year"], y=df["Simple Interest Balance"],
        name="Simple Interest (no compounding)",
        mode="lines", line=dict(color="#D85A30", dash="dash", width=2)
    ))

    fig.update_layout(barmode="stack", height=450, xaxis_title="Year", yaxis_title="Balance (₹)", yaxis_tickformat="₹,.0f")
    st.plotly_chart(fig, width='stretch')


# --- Rule of 72 ---
rule72 = round(72 / interest_rate, 1)
st.info(f"📌 **Rule of 72:** At {interest_rate}% annual return, your money doubles roughly every **{rule72} years**.")

with st.expander("📐 How is this calculated?"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        **Compound Interest Formula:**

        $$A = P \\left(1 + \\frac{{r}}{{n}}\\right)^{{nt}}$$

        | Variable | Meaning | Your Value |
        |----------|---------|------------|
        | A | Final amount | ₹{final_balance:,.2f} |
        | P | Principal (initial amount) | ₹{principal:,} |
        | r | Annual interest rate (decimal) | {r} ({interest_rate}%) |
        | n | Compounding periods per year | {n} ({freq_label}) |
        | t | Time in years | {years} |

        **Simple Interest Formula (for comparison):**

        $$A = P(1 + rt) = {principal:,} \\times (1 + {r} \\times {years}) = ₹{simple_interest_total:,.2f}$$
        """)
    with col2:
        # with st.expander("📊 View Year-by-Year Breakdown"):
        display_df = df.copy()
        display_df["Total Balance"] = display_df["Total Balance"].map("₹{:,.2f}".format)
        display_df["Principal"] = display_df["Principal"].map("₹{:,.2f}".format)
        display_df["Interest Earned"] = display_df["Interest Earned"].map("₹{:,.2f}".format)
        display_df["Simple Interest Balance"] = display_df["Simple Interest Balance"].map("₹{:,.2f}".format)
        st.dataframe(display_df, width='stretch', hide_index=True)

st.subheader(":rainbow[Step 5: Market Sectors Performance:]", divider="violet")