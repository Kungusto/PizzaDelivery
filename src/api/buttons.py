from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from src.schemas.meals import Meal

def buttons_menu(data: list[Meal]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=meal.title, callback_data=f"meal-{index}")]
            for index, meal in enumerate(data)
        ]
    )

def buttons_choise(index: int) -> InlineKeyboardMarkup: 
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Добавить в корзину", callback_data="add")],
            [InlineKeyboardButton(text="Отмена", callback_data="cancel")],
            [InlineKeyboardButton(text="Корзина", callback_data="bucket")]
        ]
    )

def buttons_bucket(data: list[Meal]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=meal.title, callback_data=f"bucket-{index}")]
            for index, meal in enumerate(data)
        ]
    )


def buttons_choise_bucket() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Удалить из корзины", callback_data="bucket")]
            [InlineKeyboardButton(text="Оформить заказ", callback_data="complete-the-order")],
            [InlineKeyboardButton(text="Отмена", callback_data="" \
            "cancel")],
        ]
    )