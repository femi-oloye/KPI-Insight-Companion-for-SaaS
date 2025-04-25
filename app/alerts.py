import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]

def detect_issues(kpis: dict) -> str:
    alert_prompt = f"""
    These are the current SaaS KPIs:

    CAC: ${kpis['CAC']}
    LTV: ${kpis['LTV']}
    Conversion Rate: {kpis['Conversion Rate']}%
    Churn Rate: {kpis['Churn Rate']}%

    Detect any anomalies or risks (e.g., high churn, low LTV).
    Suggest a specific data-driven action for each issue.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": alert_prompt}],
            temperature=0.5,
            max_tokens=250
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        st.exception(e)  # <--- Show full error traceback in app
        return "An error occurred while generating alerts."
