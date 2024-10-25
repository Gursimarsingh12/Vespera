from pydantic import BaseModel
from .projectSchema import ProjectHolding
from typing import List


class User(BaseModel):
    phone_number: str
    energy_consumption : float
    active_stocks : List[ProjectHolding] = []
    balance : float




def user_schema(user: dict) -> dict:
    return {
        "user_id": user["user_id"],
        "profile_url": user["profile_url"],
        "phone_number": user["phone_number"],
        "name": user["name"],
        "semester": user["semester"],
        "branch": user["branch"]
    }