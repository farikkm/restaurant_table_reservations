from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.keyboards.reply import main_menu_kb

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        "Привет! Я бот для бронирования столиков в ресторане.\n"
        "Выберите действие:",
        reply_markup=main_menu_kb(),
    )
