from pydantic import BaseModel
from src.schemas.meals import Meal

class Order(BaseModel):
    chat_id: int
    user_id: str


class OrderWithRels(Order):
    meals: list[Meal]