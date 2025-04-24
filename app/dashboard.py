import streamlit as st
import pandas as pd
import plotly.express as px
from kpi_engine import calculate_kpis
from gpt_summary import generate_kpi_summary
from alerts import detect_issues
import openai
import os

# Set OpenRouter API base and key
openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(page_title="SaaS KPI Agent", layout="wide")

# Load Data
df = pd.read_csv("data/mock_saas_data.csv", parse_dates=["date"])

# Calculate Monthly Subscription Fee per Active User
df["monthly_subscription_fee"] = df["revenue"] / df["active_users"]

# Calculate MRR and ARR
df["mrr"] = df["revenue"]
df["arr"] = df["mrr"] * 12

# Calculate KPIs
kpis = calculate_kpis(df)

# Show KPI Cards
st.markdown("### 📊 Key Performance Indicators")
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("CAC", f"${kpis['CAC']}")
col2.metric("LTV", f"${kpis['LTV']}")
col3.metric("Conversion Rate", f"{kpis['Conversion Rate']}%")
col4.metric("Churn Rate", f"{kpis['Churn Rate']}%")
col5.metric("MRR", f"${df['mrr'].sum():,.2f}")
col6.metric("ARR", f"${df['arr'].sum():,.2f}")

# AI Summary
st.markdown("### 🧠 AI-Generated KPI Insight")
with st.spinner("Analyzing KPIs..."):
    try:
        summary = generate_kpi_summary(kpis)
        st.info(summary)
    except Exception as e:
        st.error(f"Error generating AI summary: {e}")

# Natural Language Q&A
st.markdown("### 💬 Ask About KPIs")
user_question = st.text_input("Ask your KPI assistant...")

if user_question:
    with st.spinner("Thinking..."):
        try:
            prompt = f"""
            You are a SaaS KPI analyst. Given these metrics:

            CAC: ${kpis['CAC']}
            LTV: ${kpis['LTV']}
            Conversion Rate: {kpis['Conversion Rate']}%
            Churn Rate: {kpis['Churn Rate']}%
            MRR: ${df['mrr'].sum():,.2f}
            ARR: ${df['arr'].sum():,.2f}

            User question: {user_question}
            Answer in a clear, helpful tone.
            """
            response = openai.ChatCompletion.create(
                model="openai/gpt-3.5-turbo",  # ✅ Corrected model ID
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6,
                max_tokens=200
            )
            st.success(response.choices[0].message["content"])
        except Exception as e:
            st.error(f"Error answering question: {e}")

# AI Alerts
st.markdown("### 🔔 KPI Alerts & AI Recommendations")
with st.spinner("Scanning for risks..."):
    try:
        alerts = detect_issues(kpis)
        st.warning(alerts)
    except Exception as e:
        st.error(f"Error generating alerts: {e}")

# Tabs for Visualization
tab1, tab2 = st.tabs(["📈 Sales KPIs", "📣 Marketing KPIs"])

with tab1:
    st.subheader("Monthly Revenue")
    fig = px.line(df, x="date", y="revenue", title="Revenue Over Time")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Customer Growth")
    fig = px.bar(df, x="date", y="new_customers", title="New Customers")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Leads & Ad Spend")
    fig = px.line(df, x="date", y=["leads", "ad_spend"], title="Leads vs Ad Spend")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Email Open Rate")
    fig = px.line(df, x="date", y="email_open_rate", title="Email Open Rate Over Time")
    st.plotly_chart(fig, use_container_width=True)
