from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from database import SessionLocal
from models import Booking

router = Router()

def cancel_keyboard(booking_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌Отменить", callback_data=f"cancel_{booking_id}")]
        ]
    )

@router.callback_query(lambda c: c.data.startswith("cancel_"))
async def cancel_booking(callback: CallbackQuery):
    booking_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    session = SessionLocal()
    booking = session.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == user_id
    ).first()

    if not booking:
        await callback.answer("❌Не найдено")
        session.close()
        return

    session.delete(booking)
    session.commit()
    session.close()

    await callback.answer("❌Отменено")
    await callback.message.edit_text("✅Бронирование успешно отменено.")