from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("custom"))
async def custom_command(message: Message) -> None:
    await message.answer("")