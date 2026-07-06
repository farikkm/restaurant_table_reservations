from aiogram.fsm.state import StatesGroup, State


class BookingStates(StatesGroup):
    choosing_guests = State()
    choosing_date = State()
    choosing_time = State()
    confirming = State()
