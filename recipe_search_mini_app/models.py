from pydantic import BaseModel, Field
from typing import List, Optional

class Ingredient(BaseModel):
    name: str
    quantity: Optional[float] = None
    unit: Optional[str] = None

class Recipe(BaseModel):
    id: int
    title: str
    url: Optional[str] = None
    total_time_min: Optional[int] = None
    ingredients: List[Ingredient] = Field(default_factory=list)

class SearchRequest(BaseModel):
    query: str  # "鶏むね 長ねぎ 時短" など

