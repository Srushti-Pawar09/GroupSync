from fastapi import FastAPI
from llm_parser import parse_user_message
from recommender import recommend_destinations
from explanation import generate_explanation

app = FastAPI()

# In-memory group storage
groups = {}


@app.post("/chat")
def chat(payload: dict):

    group_id = payload["group_id"]
    user_id = payload["user_id"]
    message = payload["message"]

    parsed = parse_user_message(message)
    parsed["user_id"] = user_id

    if group_id not in groups:
        groups[group_id] = []

    # Replace if user already sent preferences
    groups[group_id] = [
        u for u in groups[group_id] if u["user_id"] != user_id
    ]

    groups[group_id].append(parsed)

    return {
        "status": "added",
        "group_id": group_id,
        "total_members": len(groups[group_id]),
        "parsed_user": parsed
    }

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

