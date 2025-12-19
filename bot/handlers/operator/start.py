from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from bot.core.db import get_session
from bot.dao.users_dao import UsersDAO

router = Router()

@router.message(Command("op"))
async def op_mode(m: Message, session: AsyncSession = get_session()):
    users = UsersDAO(session)
    u = await users.get_or_create(m.from_user.id, username=m.from_user.username, full_name=m.from_user.full_name, role="OPERATOR", is_active=True)
    await session.commit()
    await m.answer("Оператор зарегистрирован. Команды: /shift_start <адрес>, /shift_end")
