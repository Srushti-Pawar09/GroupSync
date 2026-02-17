import requests
import json

def parse_user_message(message: str):

    prompt = f"""
Extract travel preferences into JSON format:

Fields:
- budget (integer in INR)
- vibes (list of strings)
- start_city
- start_date
- end_date

User message:
{message}

Return ONLY JSON.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    text = response.json()["response"]

    return json.loads(text)
