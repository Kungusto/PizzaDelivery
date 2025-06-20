from sqlalchemy import select
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router

from src.utils.db_session import get_db
from src.schemas.meals import Meal
from src.models import *
from src.api.buttons import buttons_menu


router = Router()


@router.message(CommandStart())
async def greeting(message: Message):
    async for session in get_db():
        query = select(MealsORM)
        model = await session.execute(query)
        result = [Meal.model_validate(result, from_attributes=True) for result in model.scalars().all()]
    await message.answer("""
    🍕 Добро пожаловать в нашу пиццерию!
    Здесь всё просто: выбери пиццу, добавь в корзину и оформи заказ, и мы уже готовим!

    🥗 Только свежие ингредиенты
    🔥 Быстрая доставка
    📦 Удобный заказ прямо в Telegram

    Жми на кнопку ниже и погнали! 👇
    """,
    reply_markup=buttons_menu(result))

