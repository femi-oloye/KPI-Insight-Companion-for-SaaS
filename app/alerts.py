import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_base = "https://openrouter.ai/api/v1"
openai.api_key = os.getenv("OPENROUTER_API_KEY")

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
        print("🔔 Full alert response:", response)
        if "choices" in response:
            return response["choices"][0]["message"]["content"].strip()
        else:
            return "OpenAI returned an unexpected response. Please check your quota or model."
    except Exception as e:
        print("❌ Error generating alerts:", e)
        return f"An error occurred while generating alerts: {e}"
