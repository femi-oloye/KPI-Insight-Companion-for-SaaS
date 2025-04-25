import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = os.getenv("OPENROUTER_API_KEY")

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
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=250
        )
        print("📦 Full summary response:", response)
        if "choices" in response:
            return response["choices"][0]["message"]["content"].strip()
        else:
            return "OpenAI returned an unexpected response. Please check your API key or model settings."
    except Exception as e:
        print("❌ Error generating KPI summary:", e)
        return f"An error occurred while generating the KPI summary: {e}"
