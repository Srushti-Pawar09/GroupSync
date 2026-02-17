from typing import List
from pydantic import BaseModel

class UserPreference(BaseModel):
    budget: int
    vibes: List[str]
    start_city: str
    start_date: str
    end_date: str
