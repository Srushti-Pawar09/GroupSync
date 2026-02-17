import json
from llm_service import call_llm


def parse_user_message(message: str):

    prompt = f"""
Extract structured travel preferences from the following message.

Return ONLY valid JSON with this structure:

{{
  "budget": integer,
  "vibes": list of lowercase strings,
  "start_city": lowercase string,
  "start_date": "YYYY-MM-DD",
  "end_date": "YYYY-MM-DD",
  "group_size": integer
}}

If month is mentioned but no exact dates,
assume 3-day trip starting from 10th of that month in 2026.

Message:
{message}
"""

    raw = call_llm(prompt)

    try:
        parsed = json.loads(raw)
    except:
        raise ValueError("LLM returned invalid JSON")

    return parsed
