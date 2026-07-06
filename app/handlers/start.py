from pathlib import Path

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton

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