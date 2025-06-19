import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("etl_upi_transactions_cleaned.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M').astype(str)
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("📅 Filter Transactions")
selected_month = st.sidebar.selectbox("Select Month", sorted(df['Month'].unique(), reverse=True))
selected_category = st.sidebar.multiselect("Select Category", df['Category'].unique(), default=df['Category'].unique())

filtered_df = df[(df['Month'] == selected_month) & (df['Category'].isin(selected_category))]

# KPIs
total_spend = filtered_df['Amount'].sum()
avg_spend = filtered_df['Amount'].mean()
num_txns = filtered_df.shape[0]

# Dashboard title
st.title("📊 UPI Spend Tracker Dashboard")

# KPIs Display
st.markdown("### Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("💸 Total Spend", f"₹{total_spend:,.2f}")
col2.metric("📊 Avg. Transaction", f"₹{avg_spend:,.2f}")
col3.metric("🔁 No. of Transactions", num_txns)

# Category-wise Spend
st.markdown("### 🧾 Category-wise Spend")
cat_fig = px.pie(filtered_df, names='Category', values='Amount', title='Spend by Category')
st.plotly_chart(cat_fig, use_container_width=True)

# Monthly Spend Trend
st.markdown("### 📈 Monthly Spend Trend")
trend_df = df.groupby('Month')['Amount'].sum().reset_index()
line_fig = px.line(trend_df, x='Month', y='Amount', title='Monthly Spend Over Time', markers=True)
st.plotly_chart(line_fig, use_container_width=True)

# Raw Data
with st.expander("🧾 View Raw Transaction Data"):
    st.dataframe(filtered_df)
