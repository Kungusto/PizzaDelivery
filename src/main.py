import asyncio
from aiogram import Dispatcher, Bot
from aiogram.types import Message
import logging


# -----
import sys
from pathlib import Path

# добавление src в поле видимости
sys.path.append(str(Path(__file__).parent.parent))
# -----


from src.api.handlers import router
from src.config import settings

token = settings.API_TOKEN_TG
bot = Bot(token=token)
dp = Dispatcher()

async def main():
    await dp.start_polling(bot, skip_updates=False)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    dp.include_router(router)
    asyncio.run(main())