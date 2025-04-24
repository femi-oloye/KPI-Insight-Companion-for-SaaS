import os
import openai
from dotenv import load_dotenv
load_dotenv()

# Set the base URL for OpenRouter API
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
        response = openai.Completion.create(
            model="gpt-3.5-turbo",  # Replace this with OpenRouter's actual model name
            prompt=prompt,
            temperature=0.7,
            max_tokens=250
        )
        return response.choices[0].text.strip()

    except openai.OpenAIError as e:
        print(f"Error: {e}")
        return "An error occurred while generating the KPI summary."
