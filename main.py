import logging

from app.db.models import start_running
from app.utils.logger_config import setup_logger

from os import getenv
from dotenv import load_dotenv

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.handlers.start import router as start_router
from app.handlers.cancel_booking import router as cancel_booking_router
from app.handlers.my_bookings import router as my_bookings_router
from db_models import start_running

setup_logger()
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = getenv("BOT_TOKEN=8947871324:AAHqYGMzbOAL-urOYLWZbG7-DPGcq--Ey7k")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN is not set. Check your .env file or environment variables.")

dp = Dispatcher(storage=MemoryStorage())
dp.include_router(start_router)
dp.include_router(my_bookings_router)
dp.include_router(cancel_booking_router)

async def main() -> None:
    await start_running()
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())