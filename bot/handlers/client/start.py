from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from bot.core.db import get_session
from bot.dao.users_dao import UsersDAO
from bot.keyboards.reply.client_menu import client_menu

router = Router()

@router.message(CommandStart())
async def start(m: Message, session: AsyncSession = get_session()):
    users = UsersDAO(session)
    await users.get_or_create(m.from_user.id, username=m.from_user.username, full_name=m.from_user.full_name, role="CLIENT", is_active=True)
    await session.commit()
    await m.answer("TelegaShop ✅", reply_markup=client_menu())
