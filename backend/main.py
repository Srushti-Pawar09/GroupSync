from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from google import genai
import os
import uvicorn

from llm_parser import parse_user_input
from recommender import recommend_destinations
from explanation import generate_explanation
from llm_service import call_llm

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

client = genai.Client(api_key=GEMINI_API_KEY)

# -----------------------------
# FastAPI setup
# -----------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # restrict in production if needed
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# In-memory storage
# -----------------------------
groups = {}

# -----------------------------
# Helper: Check if group ready
# -----------------------------
def is_group_ready(preferences_dict):

    if len(preferences_dict) < 2:
        return False

    for user, prefs in preferences_dict.items():
        if not prefs.get("budget"):
            return False
        if not prefs.get("vibes"):
            return False
        if not prefs.get("start_date") or not prefs.get("end_date"):
            return False

    return True


# -----------------------------
# Chat Endpoint
# -----------------------------
@app.post("/chat")
def chat(payload: dict):

    group_id = payload["group_id"]
    username = payload["username"]
    message = payload["message"]

    group = groups.setdefault(group_id, {
        "messages": [],
        "preferences": {},
        "history": []
    })

    group["messages"].append({
        "user": username,
        "text": message
    })

    # Extract preferences
    try:
        extracted = parse_user_input(message)
    except Exception:
        extracted = {}

    if username not in group["preferences"]:
        group["preferences"][username] = {}

    group["preferences"][username].update(extracted)

    # -----------------------------------------
    # TRIGGER RECOMMENDATION
    # -----------------------------------------
    if "@bot recommend" in message.lower():

        combined = {}

        for user, prefs in group["preferences"].items():
            for key, value in prefs.items():
                combined.setdefault(key, []).append(value)

        prompt = f"""
You are a group travel planning assistant.
Given multiple users' preferences,
suggest one optimal destination.

Return:
- City
- Estimated days
- Cost per person

Speak clearly and naturally.

Group preferences:
{combined}
"""

        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )

            reply = response.text

        except Exception:
            reply = "Recommendation generation failed."

        group["history"].append({
            "role": "assistant",
            "content": reply
        })

        return {"reply": reply}

    # -----------------------------------------
    # Normal conversational reply
    # -----------------------------------------
    reply_prompt = f"""
You are a travel planning assistant in a group chat.

Current group preferences:
{group["preferences"]}

Latest message from {username}:
"{message}"

Respond conversationally.
If enough data exists, summarize current plan.
"""

    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=reply_prompt
        )

        reply = response.text

    except Exception:
        reply = "Preferences updated."

    return {"reply": reply}


# -----------------------------
# Get Group Info
# -----------------------------
@app.get("/group/{group_id}")
def get_group(group_id: str):

    if group_id not in groups:
        return {"message": "Group not found"}

    group = groups[group_id]

    return {
        "group_id": group_id,
        "members_count": len(group["preferences"]),
        "preferences": group["preferences"],
        "messages": group["messages"]
    }


# -----------------------------
# Explicit Recommend Endpoint
# -----------------------------
@app.post("/recommend")
def recommend(payload: dict):

    group_id = payload["group_id"]

    if group_id not in groups:
        return {"message": "Group not found"}

    group = groups[group_id]
    preferences = group["preferences"]

    if not is_group_ready(preferences):
        return {
            "message": "Group not ready. Waiting for complete preferences.",
            "members_count": len(preferences)
        }

    results = recommend_destinations(preferences)
    explanation = generate_explanation(results)

    return {
        "group_id": group_id,
        "members_count": len(preferences),
        "recommendations": results,
        "explanation": explanation
    }


# -----------------------------
# Entry point for local dev
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)