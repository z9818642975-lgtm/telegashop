from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router(name="start")


@router.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("Р вЂќР С•Р В±РЎР‚Р С• Р С—Р С•Р В¶Р В°Р В»Р С•Р Р†Р В°РЎвЂљРЎРЉ")

