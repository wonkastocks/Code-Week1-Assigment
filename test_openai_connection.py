import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(override=True)

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("[ERROR] OPENAI_API_KEY not found in environment variables.")
    exit(1)

openai.api_key = api_key

try:
    # A lightweight test: list available models
    models = openai.models.list()
    print("[SUCCESS] Connected to OpenAI API!")
    print(f"Number of models available: {len(models.data)}")
    print("Sample model ID:", models.data[0].id)
except Exception as e:
    print("[ERROR] Could not connect to OpenAI API.")
    print(e)
