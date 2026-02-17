from fastapi import FastAPI, Body
from llm_parser import parse_user_message
from recommender import recommend_destinations
from explanation import generate_explanation
import requests

app = FastAPI()

group_members = []

@app.post("/chat")
def chat(payload: dict = Body(...)):
    message = payload["message"]

    parsed = parse_user_message(message)
    group_members.append(parsed)

    return {"parsed": parsed}


@app.get("/recommend")
def recommend():

    results = recommend_destinations(group_members)

    explanation = generate_explanation(results)

    return {
        "recommendations": results,
        "explanation": explanation
    }



