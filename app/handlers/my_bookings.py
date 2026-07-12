from aiogram import F, Router
from aiogram.types import Message

from app.db.models import async_session, Reservation
from app.handlers.cancel_booking import cancel_keyboard
from sqlalchemy import select

router = Router()

@router.message(F.text == "📋Мои бронирования")
async def show_my_bookings(message: Message):
    user_id = message.from_user.id

    async with async_session() as session:
        stmt = select(Reservation).where(Reservation.user_id == user_id)
        result = await session.execute(stmt)
        bookings = result.scalars().all()

    if not bookings:
        await message.answer("❌ У вас нет бронирований.")
        return

    for b in bookings:
        text = (
            f"📞 Бронь #{b.id}\n"
            f"📅 Дата: {b.date}\n"
            f"⏱️ Время: {b.time}\n"
            f"🪑 Столик: {b.table_id}\n"
            f"🙎🏻‍♂️ Гости: {b.guests}\n"
            f"📄 Статус: {b.status or '✅ Активно'}"
        )
        await message.answer(text, reply_markup=cancel_keyboard(b.id))
