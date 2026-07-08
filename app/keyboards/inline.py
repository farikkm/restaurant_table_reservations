from datetime import date, timedelta

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

WEEKDAYS_RU = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]


def guests_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i in range(1, 7):
        builder.button(text=f"{i} чел.", callback_data=f"guests:{i}")
    builder.adjust(3)
    return builder.as_markup()


def dates_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    today = date.today()
    for i in range(1, 8):
        d = today + timedelta(days=i)
        label = f"{d.strftime('%d.%m')} ({WEEKDAYS_RU[d.weekday()]})"
        builder.button(text=label, callback_data=f"date:{d.isoformat()}")
    builder.adjust(2)
    return builder.as_markup()


def times_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for hour in range(12, 22):
        t = f"{hour:02d}:00"
        builder.button(text=t, callback_data=f"time:{t}")
    builder.adjust(3)
    return builder.as_markup()


def confirm_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Да", callback_data="confirm:yes")
    builder.button(text="❌ Нет", callback_data="confirm:no")
    builder.adjust(2)
    return builder.as_markup()


def my_bookings_kb(active_bookings: list[dict]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for b in active_bookings:
        builder.button(
            text=f"❌ Отменить бронь {b['date']} {b['time']}",
            callback_data=f"cancel:{b['id']}",
        )
    builder.adjust(1)
    return builder.as_markup()