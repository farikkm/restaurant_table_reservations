from pathlib import Path

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    FSInputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)
from sqlalchemy import select

from app.db.models import User, async_session
from app.handlers.register import RegisterState, register_router

router = Router()
router.include_router(register_router)

BASE_DIR = Path(__file__).resolve().parent.parent
photo_path = BASE_DIR / "img" / "images.png"


def get_start_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🍽 Забронировать столик")],
            [KeyboardButton(text="📋 Мои бронирования"), KeyboardButton(text="ℹ️ О ресторане")],
            [KeyboardButton(text="ℹ️ Помощь")],
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
    )


async def get_user_by_telegram_id(telegram_id: int):
    async with async_session() as session:
        result = await session.scalars(select(User).where(User.telegram_id == telegram_id))
        return result.first()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    user = await get_user_by_telegram_id(message.from_user.id)
    if not user:
        await state.set_state(RegisterState.name)
        await message.answer(
            "Привет! Сначала нужно зарегистрироваться. Введите, пожалуйста, своё имя."
        )
        return

    keyboard = get_start_keyboard()
    caption = "Добро пожаловать! Выберите действие:"

    if photo_path.exists():
        photo = FSInputFile(str(photo_path))
        await message.answer_photo(
            photo=photo,
            caption=caption,
            reply_markup=keyboard,
        )
    else:
        await message.answer(caption, reply_markup=keyboard)


@router.message(F.text == "ℹ️ Помощь")
async def help_handler(message: Message):
    await message.answer(
        "ℹ️ <b>Помощь</b>\n"
        "━━━━━━━━━━━━━━\n\n"
        "👤 <b>Поддержка</b>\n"
        "📩 @ofi_piko\n\n"
        "🕘 <b>График работы</b>\n"
        "• 10:00 — 01:00 (UTC+5)\n\n"
        "💡 <i>Мы обязательно ответим вам в рабочее время.</i>\n\n"
        "❤️ Спасибо, что пользуетесь нашим ботом!",
        parse_mode="HTML",
    )
