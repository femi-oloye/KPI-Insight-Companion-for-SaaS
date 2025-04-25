import openai
import streamlit as st

# Load OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

def generate_kpi_summary(kpis: dict) -> str:
    prompt = f"""
    Analyze these SaaS KPIs and provide an executive summary:

    CAC: ${kpis['CAC']}
    LTV: ${kpis['LTV']}
    Conversion Rate: {kpis['Conversion Rate']}%
    Churn Rate: {kpis['Churn Rate']}%

    Mention any major changes or possible concerns.
    Suggest one strategic action based on the data.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=250
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.OpenAIError as e:
        return "An error occurred while generating the KPI summary."
