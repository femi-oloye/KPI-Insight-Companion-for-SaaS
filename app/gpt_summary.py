import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = "https://api.openai.com/v1"

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
            model="gpt-3.5-turbo",  # OpenAI model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=250
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.OpenAIError as e:
        print(f"Error: {e}")
        return "An error occurred while generating the KPI summary."
