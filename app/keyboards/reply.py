from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_menu_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="🍽 Забронировать столик"))
    builder.add(KeyboardButton(text="📋 Мои бронирования"))
    builder.add(KeyboardButton(text="ℹ️ О ресторане"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
