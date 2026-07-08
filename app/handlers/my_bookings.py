from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message

from database import SessionLocal
from models import Booking
from cancelbooking import cancel_keyboard

router = Router()

@router.message(Text("📦Мои бронирования"))
async def show_my_bookings(message: Message):
    user_id = message.from_user.id

    session = SessionLocal()
    bookings = session.query(Booking).filter(Booking.user_id == user_id).all()
    session.close()

    if not bookings:
        await message.answer("❌У вас нет бронирований.")
        return

    for b in bookings:
        text = f"📞Бронь #{b.id}\n📅Дата: {b.date}\n⏱️Время: {b.time}\n🪑Столик: {b.table_id}\n🙎🏻‍♂️Гости: {b.guests}\n📄Статус: {b.status or '✅Активно'}"
        await message.answer(text, reply_markup=cancel_keyboard(b.id))
