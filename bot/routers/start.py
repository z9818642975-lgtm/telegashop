# bot/routers/start.py
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.dao.users_dao import UsersDAO
from bot.dao.warehouses_dao import WarehousesDAO
from bot.keyboards.admin.main import admin_main_menu_kb
from bot.keyboards.client.main import client_main_menu_kb
from bot.keyboards.operator.main import operator_main_menu_kb
from bot.models.enums import UserRole

router = Router(name="start")


@router.message(Command("debug"))
async def start(
    message: Message,
    session: AsyncSession,
):
    users = UsersDAO(session)
    user = await users.get_or_create(tg_id=message.from_user.id)

    # ================= CLIENT =================
    if user.role == UserRole.CLIENT:
        warehouses = WarehousesDAO(session)
        active = await warehouses.list_active()

        if active:
            text = (
                "👋 <b>Добро пожаловать!</b>\n\n"
                "📍 <b>Самовывоз сейчас доступен:</b>\n"
            )
            text += "\n".join(f"• {w.address}" for w in active if w.address)
        else:
            text = (
                "👋 <b>Добро пожаловать!</b>\n\n"
                "⚠ <b>Сейчас нет активных пунктов самовывоза</b>"
            )

        await message.answer(
            text,
            reply_markup=client_main_menu_kb(),
            parse_mode="HTML",
        )
        return

    # ================= OPERATOR =================
    if user.role == UserRole.OPERATOR:
        await message.answer(
            "👨‍💼 <b>Панель оператора</b>",
            reply_markup=operator_main_menu_kb(on_shift=False),
            parse_mode="HTML",
        )
        return

    # ================= ADMIN =================
    if user.role == UserRole.ADMIN:
        await message.answer(
            "👑 <b>Админ-панель</b>\nВыберите раздел:",
            reply_markup=admin_main_menu_kb(),
            parse_mode="HTML",
        )
        return
@router.message(Command("debug"))
async def debug(message: Message):
    await message.answer("DEBUG OK")