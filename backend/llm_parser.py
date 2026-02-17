import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def parse_user_message(message: str):

    prompt = f"""
Extract structured JSON from this Indian travel message.

Return ONLY valid JSON with fields:
{{
  "budget": integer,
  "vibes": list of lowercase strings,
  "start_city": string,
  "start_date": YYYY-MM-DD,
  "end_date": YYYY-MM-DD
}}

Message:
{message}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    content = response.json()["response"]

    return json.loads(content)
