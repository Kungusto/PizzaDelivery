from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from src.schemas.meals import Meal

def buttons_menu(data: list[Meal]):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=meal.title, callback_data=f"meal-{index}")]
            for index, meal in enumerate(data)
        ]
    )
