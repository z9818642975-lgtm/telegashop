from __future__ import annotations

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

router = Router(name="start")


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Добро пожаловать")

