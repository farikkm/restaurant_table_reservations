from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from app.db.models import async_session, Reservation
from sqlalchemy import select

router = Router()

def cancel_keyboard(booking_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отменить", callback_data=f"cancel_{booking_id}")]
        ]
    )

@router.callback_query(lambda c: c.data.startswith("cancel_"))
async def cancel_booking(callback: CallbackQuery):
    booking_id = int(callback.data.split("_")[1])
    user_id = callback.from_user.id

    async with async_session() as session:
        stmt = select(Reservation).where(
            Reservation.id == booking_id,
            Reservation.user_id == user_id
        )
        result = await session.execute(stmt)
        booking = result.scalar_one_or_none()

        if not booking:
            await callback.answer("❌ Не найдено")
            return

        await session.delete(booking)
        await session.commit()

    await callback.answer("✅ Отменено")
    await callback.message.edit_text("✅ Бронирование отменено.")