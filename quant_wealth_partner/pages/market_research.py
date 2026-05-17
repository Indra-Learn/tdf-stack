import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import scipy.optimize as optimize

st.set_page_config(page_title="RD XIRR Calculator", page_icon="🏦", layout="wide")

st.title("🏦 Recurring Deposit — XIRR Calculator")
st.markdown("Calculate the true annualized return (XIRR) on your Recurring Deposit, just like mutual funds report it.")

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ RD Settings")

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
        use_container_width=True,
        height=380
    )
    st.caption("🔵 Invested amount  |  🟢 Interest accrued each month")

with tab2:
    line_df = df[["Month", "Invested", "Maturity Value"]].set_index("Month")
    st.line_chart(
        line_df,
        color=["#3266ad", "#1D9E75"],
        use_container_width=True,
        height=380
    )
    st.caption("🔵 Total amount invested  |  🟢 Running maturity value")

st.divider()

# ---------------------------------------------------------------------------
# Cash Flow Table
# ---------------------------------------------------------------------------
with st.expander("📋 View Month-by-Month Cash Flow"):
    cf_df = pd.DataFrame({
        "Month": list(range(1, tenure_months + 1)),
        "Date": [str(start_date + relativedelta(months=i)) for i in range(tenure_months)],
        "Installment": [f"₹{monthly_installment:,.0f}"] * tenure_months,
        "Cumulative Invested": [f"₹{monthly_installment*(i+1):,.0f}" for i in range(tenure_months)],
        "Running Maturity Value": [f"₹{running_maturity[i+1]:,.2f}" for i in range(tenure_months)],
        "Interest So Far": [f"₹{running_interest[i+1]:,.2f}" for i in range(tenure_months)],
    })
    st.dataframe(cf_df, use_container_width=True, hide_index=True)

# ---------------------------------------------------------------------------
# XIRR Cash Flow Detail
# ---------------------------------------------------------------------------
with st.expander("💹 XIRR Cash Flow Schedule"):
    xirr_df = pd.DataFrame({
        "Date": [str(d) for d in cash_dates],
        "Cash Flow": [f"-₹{monthly_installment:,.0f}" if cf < 0 else f"+₹{cf:,.2f}" for cf in cash_flows],
        "Type": ["Investment"] * tenure_months + ["Maturity Receipt"]
    })
    st.dataframe(xirr_df, use_container_width=True, hide_index=True)

    if xirr_pct:
        st.success(f"✅ XIRR = **{xirr_pct}%** per annum — this is the single discount rate that makes the NPV of all cash flows equal to zero.")

# ---------------------------------------------------------------------------
# Formula Explanation
# ---------------------------------------------------------------------------
with st.expander("📐 How XIRR is Calculated"):
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

# ---------------------------------------------------------------------------
# Comparison: RD vs Lump Sum FD
# ---------------------------------------------------------------------------
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