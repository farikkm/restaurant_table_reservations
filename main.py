import logging
from app.utils.logger_config import setup_logger

from os import getenv
from dotenv import load_dotenv

import asyncio
from aiogram import Bot, Dispatcher

from app.handlers.start import router as start_router
from app.handlers.custom import router as custom_router

setup_logger()
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN is not set. Check your .env file or environment variables.")

dp = Dispatcher()
dp.include_router(start_router)
dp.include_router(custom_router)

async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())