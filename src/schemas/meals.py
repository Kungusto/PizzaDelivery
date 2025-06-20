from pydantic import BaseModel

class Meal(BaseModel) :
    meal_id: int 
    title: str
    description: str | None
    price: int

    