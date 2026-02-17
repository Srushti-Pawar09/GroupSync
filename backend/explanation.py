import requests

def generate_explanation(results):

    prompt = f"""
Explain why these destinations are ideal for this group.

Focus on:
- Cost fairness
- Vibe matching
- Group suitability
- Famous food

Data:
{results}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]
