from pydantic import BaseModel
from typing import List

class UserPreference(BaseModel):
    budget: int
    vibes: List[str]
    start_city: str
    start_date: str
    end_date: str

class RecommendationResponse(BaseModel):
    city: str
    place: str
    stay_days: int
    travel_cost: float
    stay_cost: float
    total_cost: float
    matched_vibes: List[str]
    famous_food: str
