from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def call_llm(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )
    return response.text