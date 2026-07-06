from pathlib import Path

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton

from app.keyboards.reply import main_menu_kb

router = Router()
BASE_DIR = Path(__file__).resolve().parent.parent
photo_path = BASE_DIR / "img" / "images.png"

@router.message(Command("start"))
async def start(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🍽 Забронировать столик", callback_data="btn1")],
            [InlineKeyboardButton(text="📋 Мои бронирования", callback_data="btn2")],
            [InlineKeyboardButton(text="ℹ️ О ресторане", callback_data="btn3")]
        ]
    )


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        "Привет! Я бот для бронирования столиков в ресторане.\n"
        "Выберите действие:",
        reply_markup=main_menu_kb(),
    )
    if photo_path.exists():
        photo = FSInputFile(str(photo_path))
        await message.answer_photo(
            photo=photo,
            reply_markup=keyboard
        )
    else:
        await message.answer(
            reply_markup=keyboard
        )
