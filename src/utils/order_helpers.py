from src.schemas.meals import Meal


def total_cost(meals: list[Meal]) -> int:
    return sum([meal.price for meal in meals])