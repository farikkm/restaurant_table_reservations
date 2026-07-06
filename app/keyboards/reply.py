from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def custom_builder() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text="❌Отменить бронирование")
    )
    builder.adjust(2)

    return builder.as_markup()