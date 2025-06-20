from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from src.schemas.meals import Meal


def buttons_menu(data: list[Meal], bucket: list[Meal] = []) -> InlineKeyboardMarkup:
    if bucket:
        list_to_add = [[InlineKeyboardButton(text=f"🗑 Корзина ({len(bucket)} шт.)", callback_data="bucket")]]
    else:
        list_to_add = []
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=meal.title, callback_data=f"meal-{index}")]
            for index, meal in enumerate(data)] + list_to_add
    )



def buttons_choise(index: int) -> InlineKeyboardMarkup: 
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Добавить в корзину", callback_data="add")],
            [InlineKeyboardButton(text="◀️ Назад", callback_data="cancel")],
        ]
    )

def buttons_bucket(data: list[Meal]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=meal.title, callback_data=f"bucket-{index}")] 
            for index, meal in enumerate(data)
        ] + [[InlineKeyboardButton(text="📋 К меню", callback_data="menu")]] + [[InlineKeyboardButton(text="✅ Оформить заказ", callback_data="complete-bucket")]]
    )


def buttons_choise_bucket() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Удалить из корзины", callback_data="delete-bucket")],
            [InlineKeyboardButton(text="◀️ Назад", callback_data="bucket")],
        ]
    )
