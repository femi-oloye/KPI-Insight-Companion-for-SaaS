import os
from dotenv import load_dotenv

load_dotenv()

print("API Key from .env:", os.getenv("OPENAI_API_KEY"))
