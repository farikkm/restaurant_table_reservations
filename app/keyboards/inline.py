from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def custom_builder() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text="👨🏿‍🍳Мои бронирования")
    )
    builder.adjust(2)

    return builder.as_markup()