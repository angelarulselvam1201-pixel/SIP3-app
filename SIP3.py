import streamlit as st
import pandas as pd
import altair as alt
import math

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(
    page_title="Advanced SIP Calculator",
    page_icon="💹",
    layout="centered",
)

# ---------------------- CUSTOM DESIGN CSS ----------------------
st.markdown("""
<style>

body {
    background-color: #f4f6fa;
}

.big-title {
    font-size: 52px;
    text-align: center;
    color: #3a7bd5;
    font-weight: 800;
    background: -webkit-linear-gradient(45deg, #3a7bd5, #00d2ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.section-box {
    background: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.08);
    margin-top: 18px;
}

.result-card {
    background: linear-gradient(135deg, #3a7bd5, #00d2ff);
    color: white;
    padding: 25px;
    border-radius: 18px;
    margin-top: 10px;
    font-size: 20px;
    font-weight: 600;
}

.stButton>button {
    background: linear-gradient(90deg, #3a7bd5, #00d2ff);
    color: white;
    border-radius: 12px;
    padding: 10px 20px;
    font-size: 18px;
    border: none;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #205bb5, #00a2ff);
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ---------------------- HEADER ----------------------
st.markdown("<h1 class='big-title'>SIP Calculator</h1>", unsafe_allow_html=True)
st.write("<p style='text-align:center;'>💰 Smart, clean & beautiful SIP investment planner with inflation adjustment.</p>", unsafe_allow_html=True)

# ---------------------- INPUT SECTION ----------------------
st.markdown("<div class='section-box'>", unsafe_allow_html=True)
st.header("Enter Investment Details")

col1, col2 = st.columns(2)

with col1:
    monthly_sip = st.number_input("Monthly SIP Amount (₹)", min_value=100, value=5000, step=100)
    years = st.number_input("Investment Duration (Years)", min_value=1, value=10)

with col2:
    annual_return = st.number_input("Expected Annual Return (%)", min_value=1.0, value=12.0)
    inflation_rate = st.number_input("Expected Inflation Rate (%)", min_value=0.0, value=6.0)

st.markdown("</div>", unsafe_allow_html=True)

# ------------------------- FORMULAS -------------------------
def sip_future_value(P, r, yrs):
    monthly_rate = r / 12
    months = yrs * 12
    fv = P * (((1 + monthly_rate)**months - 1) / monthly_rate) * (1 + monthly_rate)
    return fv

def inflation_adjust(amount, inflation, yrs):
    return amount / ((1 + inflation)**yrs)

def sip_schedule(P, r, yrs):
    monthly_rate = r / 12
    months = yrs * 12
    data = []
    balance = 0
    invested = 0

    for month in range(1, months + 1):
        invested += P
        balance = (balance + P) * (1 + monthly_rate)
        data.append([month, invested, balance])

    return pd.DataFrame(data, columns=["Month", "Total Invested", "Future Value"])

# ---------------------- CALCULATE BUTTON ----------------------
if st.button("Calculate SIP Results"):

    df = sip_schedule(monthly_sip, annual_return/100, years)

    total_invested = monthly_sip * years * 12
    fv = sip_future_value(monthly_sip, annual_return/100, years)
    fv_infl_adj = inflation_adjust(fv, inflation_rate/100, years)
    lumpsum = total_invested * (1 + annual_return/100)**years

    # ---------------------- RESULTS CARD ----------------------
    st.markdown("<div class='section-box'>", unsafe_allow_html=True)
    st.subheader("📘 Summary of Results")

    st.markdown(f"""
    <div class='result-card'>
        Total Invested:  ₹{total_invested:,.2f}<br>
        Future Value (No Inflation):  ₹{fv:,.2f}<br>
        Inflation-Adjusted Value:  ₹{fv_infl_adj:,.2f}<br>
        Lumpsum Value (If invested once): ₹{lumpsum:,.2f}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------- CHART 1 ----------------------
    st.markdown("<div class='section-box'>", unsafe_allow_html=True)
    st.subheader("📈 SIP Growth Over Time")

    chart1 = alt.Chart(df).mark_line(color="#3a7bd5", strokeWidth=3).encode(
        x="Month",
        y="Future Value",
        tooltip=["Month", "Future Value"]
    ).interactive()

    st.altair_chart(chart1, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------- CHART 2 ----------------------
    st.markdown("<div class='section-box'>", unsafe_allow_html=True)
    st.subheader("📉 Inflation Impact Comparison")

    df_inf = pd.DataFrame({
        "Category": ["Future Value", "After Inflation"],
        "Amount": [fv, fv_infl_adj]
    })

    chart2 = alt.Chart(df_inf).mark_bar(size=70).encode(
        x="Category",
        y="Amount",
        color=alt
