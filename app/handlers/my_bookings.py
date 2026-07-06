from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from app.keyboards.inline import my_bookings_kb
from app.storage.db import get_user_bookings, cancel_booking

router = Router()

STATUS_LABELS = {
    "pending": "⏳ Ожидает",
    "confirmed": "✅ Подтверждено",
    "cancelled": "❌ Отменено",
}


def _build_bookings_text(user_id: int) -> tuple[str, list[dict]]:
    all_bookings = get_user_bookings(user_id)
    active = [b for b in all_bookings if b["status"] != "cancelled"]

    if not all_bookings:
        return "У вас пока нет бронирований.", []

    lines = ["📋 Ваши бронирования:\n"]
    for b in all_bookings:
        status = STATUS_LABELS.get(b["status"], b["status"])
        lines.append(f"#{b['id']} | {b['date']} {b['time']} | {b['guests']} гостей | {status}")

    return "\n".join(lines), active


@router.message(F.text == "📋 Мои бронирования")
async def show_my_bookings(message: Message) -> None:
    text, active = _build_bookings_text(message.from_user.id)
    markup = my_bookings_kb(active) if active else None
    await message.answer(text, reply_markup=markup)


@router.callback_query(F.data.startswith("cancel:"))
async def cancel_user_booking(callback: CallbackQuery) -> None:
    booking_id = callback.data.split(":")[1]
    success = cancel_booking(callback.from_user.id, booking_id)

    if not success:
        await callback.answer("Не удалось отменить бронирование.", show_alert=True)
        return

    await callback.answer("Бронирование отменено.", show_alert=True)
    text, active = _build_bookings_text(callback.from_user.id)
    markup = my_bookings_kb(active) if active else None
    await callback.message.edit_text(text, reply_markup=markup)
