import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def generate_explanation(results):

    prompt = f"""
Explain why these destinations are suitable for the group.

Focus on:
- Matched vibes
- Budget fairness
- Group suitability
- Famous local food

Be conversational but concise.

Data:
{results}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]
