from fastapi import FastAPI
from llm_parser import parse_user_input
from recommender import recommend_destinations
from explanation import generate_explanation
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
from llm_service import call_llm
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# In-memory group storage
groups = {}

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # TEMPORARY for testing
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
def chat(payload: dict):
    group_id = payload["group_id"]
    username = payload["username"]
    message = payload["message"]

    group = groups.setdefault(group_id, {
        "messages": [],
        "preferences": {}
    })

    group["messages"].append({
        "user": username,
        "text": message
    })

    # Parse structured data safely
    try:
        extracted = parse_user_input(message)
    except:
        extracted = {}

    if username not in group["preferences"]:
        group["preferences"][username] = {}

    group["preferences"][username].update(extracted)

    # 🧠 Generate conversational reply using phi3
    reply_prompt = f"""
    You are a friendly travel planning assistant in a group chat.

    Current group preferences:
    {group["preferences"]}

    Latest message from {username}:
    "{message}"

    Respond conversationally.
    If enough data exists, summarize the group’s current plan.
    """

    try:
        reply = call_llm(reply_prompt)
    except:
        reply = "Preferences updated."

    return {"reply": reply}



    # 🔥 TRIGGER CONDITION
    if "@bot recommend" in message.lower():

        # Aggregate preferences across users
        combined = {}

        for user, prefs in group["preferences"].items():
            for key, value in prefs.items():
                if key not in combined:
                    combined[key] = []
                combined[key].append(value)

        # Send aggregated info to LLM
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
You are a group travel planning assistant.
Given multiple users' preferences,
suggest one optimal destination.
Return city, estimated days, cost per person.
Speak clearly and naturally.
"""
                },
                {
                    "role": "user",
                    "content": f"Group preferences: {combined}"
                }
            ]
        )

        reply = response.choices[0].message.content

        group["history"].append({
            "role": "assistant",
            "content": reply
        })

        return {"reply": reply}

    return {"reply": None}




def is_group_ready(users):

    if len(users) < 2:
        return False

    for u in users:
        if not u.get("budget"):
            return False
        if not u.get("vibes"):
            return False
        if not u.get("start_date") or not u.get("end_date"):
            return False

    return True

@app.get("/group/{group_id}")
def get_group(group_id: str):

    if group_id not in groups:
        return {"message": "Group not found"}

    return {
        "group_id": group_id,
        "members_count": len(groups[group_id]),
        "members": groups[group_id]
    }


@app.post("/recommend")
def recommend(payload: dict):

    group_id = payload["group_id"]

    if group_id not in groups or not groups[group_id]:
        return {"message": "No preferences found for this group."}

    users = groups[group_id]

    if not is_group_ready(users):
        return {
            "message": "Group not ready. Waiting for more complete preferences.",
            "members_count": len(users)
        }

    results = recommend_destinations(users)
    explanation = generate_explanation(results)

    return {
        "group_id": group_id,
        "members_count": len(users),
        "recommendations": results,
        "explanation": explanation
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

