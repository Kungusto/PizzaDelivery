import logging
from sqlalchemy import select
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Router, F

from src.utils.db_session import get_db
from src.schemas.meals import Meal
from src.models import *
from src.api.buttons import buttons_menu, buttons_choise, buttons_bucket, buttons_choise_bucket
from src.utils.payment import create
from src.utils.order_helpers import total_cost

router = Router()


class Pizza(StatesGroup):
    menu = State()


@router.message(CommandStart())
async def greeting(message: Message, state: FSMContext):
    async for session in get_db():
        query = select(MealsORM)
        model = await session.execute(query)
        meals = [Meal.model_validate(result, from_attributes=True) for result in model.scalars().all()]
    await state.set_data({"meals":meals})
    await state.update_data({"bucket":[]})
    await message.answer("""
    🍕 Добро пожаловать в нашу пиццерию!
    Здесь всё просто: выбери пиццу, добавь в корзину и оформи заказ, и мы уже готовим!

    🥗 Только свежие ингредиенты
    🔥 Быстрая доставка
    📦 Удобный заказ прямо в Telegram

    Выбери пиццу, которая тебя интерисует! 👇
    """,
    reply_markup=buttons_menu(meals))


@router.callback_query(F.data.startswith("meal-"))
async def choise_meal(callback: CallbackQuery, state: FSMContext): 
    index = int(callback.data.split("-")[-1])
    meals: list = (await state.get_data())["meals"]
    choiced_meal = meals[index]
    text = f"{choiced_meal.title} - {choiced_meal.price}₽\n\t\t{choiced_meal.description}"
    buttons = buttons_choise()
    await state.update_data({"meal_now":choiced_meal})
    await callback.message.edit_text(text=text, reply_markup=buttons)


@router.callback_query(F.data.startswith("bucket-"))
async def choise(callback: CallbackQuery, state: FSMContext): 
    data = await state.get_data()
    index = int(callback.data.split("-")[-1])
    bucket: list = (await state.get_data())["bucket"]
    choiced_meal = bucket[index]
    text = f"{choiced_meal.title} - {choiced_meal.price}₽\n\t\t{choiced_meal.description}"
    await state.update_data({"current_meal_index":index})
    await callback.message.edit_text(text=text, reply_markup=buttons_choise_bucket())


@router.callback_query(F.data == "cancel")
async def cancel(callback: CallbackQuery, state: FSMContext): 
    data = await state.get_data()
    meals = data["meals"]
    bucket = data["bucket"]
    buttons = buttons_menu(data=meals, bucket=bucket)
    await callback.message.edit_text(
        text="Выберите интересующую вас пиццу 👇",
        reply_markup=buttons
    )


@router.callback_query(F.data == "add")
async def add(callback: CallbackQuery, state: FSMContext): 
    data = await state.get_data()
    meals = data["meals"]
    meal_now = data["meal_now"]
    bucket = data["bucket"]
    bucket.append(meal_now)
    await state.update_data({"bucket": bucket})
    buttons = buttons_menu(data=meals, bucket=bucket)
    await callback.message.edit_text(
        text="Выберите интересующую вас пиццу 👇",
        reply_markup=buttons
    )


@router.callback_query(F.data == "bucket")
async def bucket(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    bucket = data["bucket"]
    buttons = buttons_bucket(bucket)
    await callback.message.edit_text(
        text="Ваша текущая корзина",
        reply_markup=buttons
    )


@router.callback_query(F.data == "delete-bucket")
async def bucket_delete(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    bucket = data["bucket"]
    index = data["current_meal_index"]
    bucket.pop(index)
    await state.update_data({"bucket": bucket})
    buttons = buttons_bucket(bucket)
    await callback.message.edit_text(
        text="Ваша текущая корзина",
        reply_markup=buttons
    )
    

@router.callback_query(F.data == "menu")
async def menu(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    meals = data["meals"]
    bucket = data["bucket"]
    buttons = buttons_menu(data=meals, bucket=bucket)
    await callback.message.edit_text(
        text="Выберите интересующую вас пиццу 👇",
        reply_markup=buttons
    )


@router.callback_query(F.data == "complete-order")
async def complete_order(callback: CallbackQuery, state: FSMContext, message: Message): 
    data = await state.get_data()
    bucket = data["bucket"]
    amount = total_cost(bucket)
    chat_id = callback.message.chat.id
    url, payment_id = create(chat_id=chat_id, amount=amount, description="Заказ лучшей пиццы в городе! 🍕")
    await message.answer(f"С вас {amount}₽. Оплатить можно тут: {url}")
