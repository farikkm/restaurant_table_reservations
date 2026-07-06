from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.states.booking import BookingStates
from app.keyboards.inline import guests_kb, dates_kb, times_kb, confirm_kb
from app.storage.db import add_booking

router = Router()


@router.message(F.text == "🍽 Забронировать столик")
async def start_booking(message: Message, state: FSMContext) -> None:
    await state.set_state(BookingStates.choosing_guests)
    await message.answer("Выберите количество гостей:", reply_markup=guests_kb())


@router.callback_query(BookingStates.choosing_guests, F.data.startswith("guests:"))
async def choose_guests(callback: CallbackQuery, state: FSMContext) -> None:
    guests = int(callback.data.split(":")[1])
    await state.update_data(guests=guests)
    await state.set_state(BookingStates.choosing_date)
    await callback.message.edit_text("Выберите дату:", reply_markup=dates_kb())
    await callback.answer()


@router.callback_query(BookingStates.choosing_date, F.data.startswith("date:"))
async def choose_date(callback: CallbackQuery, state: FSMContext) -> None:
    chosen_date = callback.data.split(":", 1)[1]
    await state.update_data(date=chosen_date)
    await state.set_state(BookingStates.choosing_time)
    await callback.message.edit_text("Выберите время:", reply_markup=times_kb())
    await callback.answer()


@router.callback_query(BookingStates.choosing_time, F.data.startswith("time:"))
async def choose_time(callback: CallbackQuery, state: FSMContext) -> None:
    chosen_time = callback.data.split(":", 1)[1]
    await state.update_data(time=chosen_time)
    await state.set_state(BookingStates.confirming)

    data = await state.get_data()
    text = (
        "📋 Подтвердите бронирование:\n\n"
        f"👥 Гостей: {data['guests']}\n"
        f"📅 Дата: {data['date']}\n"
        f"🕐 Время: {data['time']}\n"
    )
    await callback.message.edit_text(text, reply_markup=confirm_kb())
    await callback.answer()


@router.callback_query(BookingStates.confirming, F.data == "confirm:yes")
async def confirm_booking(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    booking_id = add_booking(
        user_id=callback.from_user.id,
        guests=data["guests"],
        date=data["date"],
        time=data["time"],
    )
    await state.clear()
    await callback.message.edit_text(
        f"✅ Бронирование #{booking_id} оформлено!\n"
        f"Ждём вас {data['date']} в {data['time']}."
    )
    await callback.answer()


@router.callback_query(BookingStates.confirming, F.data == "confirm:no")
async def cancel_booking_fsm(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text("❌ Бронирование отменено.")
    await callback.answer()
