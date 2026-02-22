import json
from llm_service import call_llm
import re

def extract_json(text):
    """
    Extract first JSON object from LLM response.
    """
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)
    return None


def parse_user_input(message: str):
    prompt = f"""
    Extract travel preferences from the message below.
    Return ONLY valid JSON.
    
    Required format:
    {{
      "budget": number or null,
      "vibe": list of strings,
      "start_city": string or null,
      "dates": string or null
    }}

    Message:
    {message}
    """

    raw = call_llm(prompt)

    if not raw:
        return {}

    json_text = extract_json(raw)

    if not json_text:
        return {}

    try:
        return json.loads(json_text)
    except:
        return {}
