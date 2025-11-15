import streamlit as st
import pandas as pd
import altair as alt
import math

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="SIP & Inflation Calculator", layout="centered")
st.markdown("""
    <h1 style='text-align:center; color:#4CAF50;'>📈 SIP Calculator with Inflation Adjustment</h1>
""", unsafe_allow_html=True)

# -------------------- INPUT SIDEBAR --------------------
st.sidebar.header("🔧 Input Options")

monthly_invest = st.sidebar.number_input("Monthly SIP Amount (₹)", 100, 1000000, 5000)
years = st.sidebar.number_input("Investment Duration (Years)", 1, 50, 10)
expected_return = st.sidebar.slider("Expected Annual Return (%)", 1.0, 30.0, 12.0)
inflation = st.sidebar.slider("Annual Inflation Rate (%)", 0.0, 15.0, 5.0)

stepup = st.sidebar.slider("Annual SIP Step-up (%)", 0, 50, 0)
show_table = st.sidebar.checkbox("Show Yearly Breakdown Table", False)

months = years * 12
monthly_rate = expected_return / 12 / 100
inflation_rate = inflation / 100

# -------------------- CALCULATION --------------------
investment = 0
future_value = 0
adjusted_value = 0
monthly_sip = monthly_invest

yearly_rows = []

for year in range(1, years + 1):
    for m in range(12):
        investment += monthly_sip
        future_value = future_value * (1 + monthly_rate) + monthly_sip
    
    # After inflation adjustment
    adjusted_value = future_value / ((1 + inflation_rate) ** year)

    yearly_rows.append([year, round(investment), round(future_value), round(adjusted_value)])

    # Apply step-up each year
    monthly_sip *= (1 + stepup / 100)

df = pd.DataFrame(yearly_rows,
                  columns=["Year", "Total Invested (₹)", "Future Value (₹)", "Value After Inflation (₹)"])

# -------------------- METRICS DISPLAY --------------------
c1, c2, c3 = st.columns(3)

c1.metric("💰 Total Invested", f"₹{df['Total Invested (₹)'].iloc[-1]:,}")
c2.metric("🎉 Final Returns", f"₹{df['Future Value (₹)'].iloc[-1]:,}")
c3.metric("📉 Inflation Adjusted Value", f"₹{df['Value After Inflation (₹)'].iloc[-1]:,}")

st.markdown("<hr>", unsafe_allow_html=True)

# -------------------- CHARTS --------------------
st.subheader("📊 Growth of Your Investment")

line_chart = alt.Chart(df).mark_line(point=True, color="#4CAF50", strokeWidth=3).encode(
    x=alt.X("Year:O", title="Year"),
    y=alt.Y("Future Value (₹):Q", title="Value (₹)")
).properties(height=350)

st.altair_chart(line_chart, use_container_width=True)

# Inflation chart
st.subheader("📉 Inflation Adjusted Returns")

infl_chart = alt.Chart(df).mark_line(point=True, color="#FF5733", strokeWidth=3).encode(
    x="Year:O",
    y="Value After Inflation (₹):Q"
).properties(height=350)

st.altair_chart(infl_chart, use_container_width=True)

# Investment vs Returns
st.subheader("📘 Investment vs Returns Breakdown")

df_bar = pd.DataFrame({
    "Type": ["Total Invested", "Returns Gained"],
    "Amount": [
        df["Total Invested (₹)"].iloc[-1],
        df["Future Value (₹)"].iloc[-1] - df["Total Invested (₹)"].iloc[-1],
    ]
})

bar_chart = alt.Chart(df_bar).mark_bar(size=60).encode(
    x="Type:N",
    y="Amount:Q",
    color=alt.Color("Type:N",
                    scale=alt.Scale(range=["#1976D2", "#FF9800"]))
).properties(height=300)

st.altair_chart(bar_chart, use_container_width=True)

# -------------------- OPTIONAL TABLE --------------------
if show_table:
    st.subheader("📄 Yearly Breakdown Table")
    st.dataframe(df)

# -------------------- FOOTER --------------------
st.markdown("""
    <hr>
    <p style='text-align:center; color:gray;'>🚀 Built with Streamlit | SIP + Inflation + Step-Up Calculator</p>
""", unsafe_allow_html=True)
