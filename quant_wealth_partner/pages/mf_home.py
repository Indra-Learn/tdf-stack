import pandas as pd
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import scipy.optimize as optimize
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


st.subheader(":rainbow[Step 5: Recurring Deposit — XIRR Calculator]", divider="violet")
st.markdown("Calculate the true annualized return (XIRR) on your Recurring Deposit, just like mutual funds report it.")
col1, col2 = st.columns([1, 3], border=True)

with col1:
    monthly_installment = st.number_input(
        "Monthly Installment (₹)",
        min_value=500,
        max_value=500000,
        value=5000,
        step=500,
        format="%d"
    )

    tenure_months = st.slider(
        "Tenure (Months)",
        min_value=3,
        max_value=120,
        value=24,
        step=1
    )

    annual_rate = st.slider(
        "Annual Interest Rate (%)",
        min_value=1.0,
        max_value=15.0,
        value=7.0,
        step=0.25,
        format="%.2f%%"
    )

    compounding = st.selectbox(
        "Compounding Frequency",
        options=["Quarterly", "Monthly", "Yearly"],
        index=0
    )

    start_date = st.date_input(
        "Start Date",
        value=date.today().replace(day=1)
    )

with col2:
    # ---------------------------------------------------------------------------
    # RD Maturity Calculation  (standard bank formula)
    # A = P * [(1 + r/n)^(nt) - 1] / [1 - (1 + r/n)^(-1/3)]
    # We calculate each installment's maturity separately and sum.
    # ---------------------------------------------------------------------------
    comp_map = {"Quarterly": 4, "Monthly": 12, "Yearly": 1}
    n = comp_map[compounding]
    r = annual_rate / 100

    # Each installment matures for a different number of months
    maturity_values = []
    for i in range(tenure_months):
        months_remaining = tenure_months - i
        t = months_remaining / 12
        maturity = monthly_installment * (1 + r / n) ** (n * t)
        maturity_values.append(round(maturity, 2))

    total_invested = monthly_installment * tenure_months
    maturity_amount = round(sum(maturity_values), 2)
    total_interest = round(maturity_amount - total_invested, 2)

    # ---------------------------------------------------------------------------
    # XIRR Calculation
    # Cash flows: negative on each installment date, positive at maturity
    # ---------------------------------------------------------------------------
    cash_flows = []
    cash_dates = []

    for i in range(tenure_months):
        cf_date = start_date + relativedelta(months=i)
        cash_flows.append(-monthly_installment)
        cash_dates.append(cf_date)

    maturity_date = start_date + relativedelta(months=tenure_months)
    cash_flows.append(maturity_amount)
    cash_dates.append(maturity_date)

    def xirr(cash_flows, dates, guess=0.1):
        """Calculate XIRR given cash flows and dates."""
        def npv(rate):
            t0 = dates[0]
            return sum(
                cf / (1 + rate) ** ((d - t0).days / 365)
                for cf, d in zip(cash_flows, dates)
            )
        try:
            result = optimize.brentq(npv, -0.999, 100, maxiter=1000)
            return result
        except Exception:
            return None

    xirr_rate = xirr(cash_flows, cash_dates)
    xirr_pct = round(xirr_rate * 100, 2) if xirr_rate else None

    # ---------------------------------------------------------------------------
    # Metric Cards
    # ---------------------------------------------------------------------------
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Invested", f"₹{total_invested:,.0f}")
    with col2:
        st.metric("Maturity Amount", f"₹{maturity_amount:,.0f}",
                delta=f"+₹{total_interest:,.0f} interest")
    with col3:
        st.metric("Interest Earned", f"₹{total_interest:,.0f}",
                delta=f"{round(total_interest/total_invested*100,1)}% absolute return")
    with col4:
        if xirr_pct:
            st.metric("XIRR", f"{xirr_pct}%", delta="Annualized return")
        else:
            st.metric("XIRR", "N/A")

    st.divider()

    # ---------------------------------------------------------------------------
    # Build cumulative data for charts
    # ---------------------------------------------------------------------------
    months = list(range(0, tenure_months + 1))
    cum_invested = [monthly_installment * m for m in months]

    # Running maturity value if you were to close at each month
    running_maturity = [0]
    for m in range(1, tenure_months + 1):
        val = 0
        for i in range(m):
            months_remaining = m - i
            t = months_remaining / 12
            val += monthly_installment * (1 + r / n) ** (n * t)
        running_maturity.append(round(val, 2))

    running_interest = [mv - ci for mv, ci in zip(running_maturity, cum_invested)]

    df = pd.DataFrame({
        "Month": months,
        "Invested": cum_invested,
        "Interest Accrued": running_interest,
        "Maturity Value": running_maturity
    })

    # ---------------------------------------------------------------------------
    # Charts
    # ---------------------------------------------------------------------------
    st.subheader("📈 Growth Over Time")

    tab1, tab2 = st.tabs(["Bar Chart (Invested vs Interest)", "Line Chart (Value Growth)"])

    with tab1:
        bar_df = df[["Month", "Invested", "Interest Accrued"]].set_index("Month")
        st.bar_chart(
            bar_df,
            color=["#3266ad", "#1D9E75"],
            width='stretch',
            height=380
        )
        st.caption("🔵 Invested amount  |  🟢 Interest accrued each month")

    with tab2:
        line_df = df[["Month", "Invested", "Maturity Value"]].set_index("Month")
        st.line_chart(
            line_df,
            color=["#3266ad", "#1D9E75"],
            width='stretch',
            height=380
        )
        st.caption("🔵 Total amount invested  |  🟢 Running maturity value")

    st.divider()
with st.expander("📐 How is this calculated?"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            **XIRR** finds the rate `r` that satisfies:

            $$\\sum_{{i=0}}^{{n}} \\frac{{CF_i}}{{(1+r)^{{d_i/365}}}} = 0$$

            Where:
            - $CF_i$ = cash flow at period i (negative = outflow, positive = inflow)
            - $d_i$ = number of days from the first cash flow date
            - $r$ = XIRR (annualized rate we solve for)

            **Your RD Summary:**

            | Parameter | Value |
            |-----------|-------|
            | Monthly Installment | ₹{monthly_installment:,} |
            | Tenure | {tenure_months} months |
            | Annual Rate (nominal) | {annual_rate}% ({compounding}) |
            | Total Invested | ₹{total_invested:,} |
            | Maturity Amount | ₹{maturity_amount:,} |
            | XIRR | {xirr_pct}% p.a. |

            > 💡 XIRR accounts for the **timing** of each installment. Early installments compound longer,
            > later ones compound less — XIRR gives one rate that represents the true annualized return across all of them.
        """)
    with col2:
        st.write("📋 View Month-by-Month Cash Flow")
        cf_df = pd.DataFrame({
            "Month": list(range(1, tenure_months + 1)),
            "Date": [str(start_date + relativedelta(months=i)) for i in range(tenure_months)],
            "Installment": [f"₹{monthly_installment:,.0f}"] * tenure_months,
            "Cumulative Invested": [f"₹{monthly_installment*(i+1):,.0f}" for i in range(tenure_months)],
            "Running Maturity Value": [f"₹{running_maturity[i+1]:,.2f}" for i in range(tenure_months)],
            "Interest So Far": [f"₹{running_interest[i+1]:,.2f}" for i in range(tenure_months)],
        })
        st.dataframe(cf_df, width='stretch', hide_index=True)

        # ---------------------------------------------------------------------------
        # XIRR Cash Flow Detail
        # ---------------------------------------------------------------------------
        # with st.expander("💹 XIRR Cash Flow Schedule"):
        #     xirr_df = pd.DataFrame({
        #         "Date": [str(d) for d in cash_dates],
        #         "Cash Flow": [f"-₹{monthly_installment:,.0f}" if cf < 0 else f"+₹{cf:,.2f}" for cf in cash_flows],
        #         "Type": ["Investment"] * tenure_months + ["Maturity Receipt"]
        #     })
        #     st.dataframe(xirr_df, width='stretch', hide_index=True)

        #     if xirr_pct:
        #         st.success(f"✅ XIRR = **{xirr_pct}%** per annum — this is the single discount rate that makes the NPV of all cash flows equal to zero.")


with st.expander("⚖️ RD vs Lump Sum FD Comparison"):
    lumpsum = total_invested
    fd_maturity = round(lumpsum * (1 + r / n) ** (n * tenure_months / 12), 2)
    fd_interest = round(fd_maturity - lumpsum, 2)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 📅 Recurring Deposit")
        st.metric("Maturity", f"₹{maturity_amount:,.2f}")
        st.metric("Interest", f"₹{total_interest:,.2f}")
        st.metric("XIRR", f"{xirr_pct}%")

    with c2:
        st.markdown("### 💼 Lump Sum FD (same total amount)")
        st.metric("Maturity", f"₹{fd_maturity:,.2f}")
        st.metric("Interest", f"₹{fd_interest:,.2f}")
        st.metric("Rate", f"{annual_rate}%")

    st.info(f"💡 Lump sum FD earns ₹{fd_interest - total_interest:,.2f} more because the entire amount compounds from day one. In RD, installments are added gradually.")


st.subheader(":rainbow[Step 6: Smart Goal Planner]", divider="violet")

# --- Step 1: Identify the Event ---
event = st.selectbox(
    "1. Identify the Event",
    ["Child Education", "Retirement", "International Holiday", "Medical Emergency"]
)

# --- Step 2: Dynamic Priority Engine ---
# The UI reacts automatically based on the architected business rules
st.markdown("**2. Priority Status:**")
if event == "Child Education":
    st.error("🚨 **Top Priority:** Non-negotiable timeline.")
elif event == "Retirement":
    st.warning("⚠️ **High Priority:** Important, but timeline has slight flexibility compared to education.")
elif event == "International Holiday":
    st.info("🟢 **Discretionary Priority:** Can be delayed if required.")
elif event == "Medical Emergency":
    st.error("🏥 **Critical Priority:** Anytime emergency. Requires instant liquidity.")

st.write("") # Spacer

# --- Step 3: Timeline & Maturity ---
timeline = st.radio(
    "3. Timeline & Maturity Amount",
    ["Short Term (1-3 Years)", "Mid Term (3-8 Years)", "Long Term (8+ Years)"],
    horizontal=True
)

st.divider()

# --- Step 4: Action / Suggestion Engine ---
# In your architecture, this button would trigger a LangGraph Agent via FastAPI
if st.button("💡 Generate Mutual Fund Strategy", use_container_width=True):
    st.markdown(f"### Recommended Asset Allocation for: {event}")
    
    # Custom Override for Medical (Always Liquid)
    if event == "Medical Emergency":
        st.success("""
        **Emergency Corpus Strategy (Instant Liquidity & Zero Exit Load):**
        * 80% Liquid Funds 
        * 20% Overnight Funds
        """)
        
    # Standard Timeline-Based Allocation
    elif "Short Term" in timeline:
        st.info("""
        **Capital Preservation Strategy (Low Volatility):**
        * 60% Short Duration / Low Duration Debt Funds
        * 40% Arbitrage Funds
        * *Avoid pure equity to prevent capital erosion near maturity.*
        """)
        
    elif "Mid Term" in timeline:
        st.warning("""
        **Balanced Growth Strategy (Moderate Volatility):**
        * 50% Balanced Advantage Funds (BAF)
        * 30% Flexi-Cap Equity Funds
        * 20% Corporate Bond Funds
        """)
        
    elif "Long Term" in timeline:
        st.success("""
        **Wealth Creation Strategy (High Volatility, High Return):**
        * 50% Nifty 50 / Nifty Next 50 Index Funds
        * 30% Mid Cap Equity Funds
        * 20% Small Cap Equity Funds
        """)