from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router(name="start")


@router.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("Добро пожаловать")

