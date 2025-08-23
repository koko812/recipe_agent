# schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional

class RecipeQuery(BaseModel):
    ingredients: List[str] = Field(default_factory=list)   # ["鶏むね肉", "長ねぎ"]
    constraints: List[str] = Field(default_factory=list)   # ["時短", "低脂質"]
    servings: Optional[int] = 2

class Plan(BaseModel):
    steps: List[str]

class RecipeCandidate(BaseModel):
    title: str
    url: str
    ingredients: List[str]
    summary: str
    score: float

class AgentReply(BaseModel):
    plan: Plan
    choices: List[RecipeCandidate]
    final_answer: str

