from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from sqlalchemy import select

from app.db.models import User, async_session

register_router = Router()


class RegisterState(StatesGroup):
    name = State()
    phone = State()


async def get_user_by_telegram_id(telegram_id: int):
    async with async_session() as session:
        result = await session.scalars(select(User).where(User.telegram_id == telegram_id))
        return result.first()


async def save_user(telegram_id: int, full_name: str, phone: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == telegram_id))
        if user:
            user.full_name = full_name
            user.username = phone
        else:
            session.add(
                User(
                    telegram_id=telegram_id,
                    full_name=full_name,
                    username=phone,
                    role="user",
                )
            )
        await session.commit()


@register_router.message(RegisterState.name)
async def register_name_handler(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Отправить номер", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    await state.set_state(RegisterState.phone)
    await message.answer(
        "Спасибо! Теперь отправьте, пожалуйста, свой номер телефона.",
        reply_markup=keyboard,
    )


@register_router.message(RegisterState.phone, F.content_type == "contact")
async def register_phone_contact_handler(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    data = await state.get_data()
    await save_user(message.from_user.id, data["full_name"], phone)
    await state.clear()
    await message.answer(
        f"Регистрация завершена, {data['full_name']}! Теперь вы можете забронировать столик.",
        reply_markup=ReplyKeyboardRemove(),
    )


@register_router.message(RegisterState.phone)
async def register_phone_text_handler(message: Message, state: FSMContext):
    phone = message.text.strip()
    if not phone:
        await message.answer("Пожалуйста, отправьте номер телефона или нажмите кнопку для контактных данных.")
        return

    data = await state.get_data()
    await save_user(message.from_user.id, data["full_name"], phone)
    await state.clear()
    await message.answer(
        f"Регистрация завершена, {data['full_name']}! Теперь вы можете забронировать столик.",
        reply_markup=ReplyKeyboardRemove(),
    )
