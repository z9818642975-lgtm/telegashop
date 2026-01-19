from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.dao.users_dao import UsersDAO
from bot.dao.warehouses_dao import WarehousesDAO

from bot.keyboards.client.main import client_main_menu
from bot.keyboards.operator.main import operator_main_menu
from bot.keyboards.admin.main import admin_main_menu

from bot.utils.safe_edit import safe_edit_text

router = Router(name="start")


@router.message(CommandStart())
async def start(
    message: Message,
    session: AsyncSession,
):
    users = UsersDAO(session)
    user = await users.get_or_create(message.from_user)

    # =====================================================
    # CLIENT
    # =====================================================
    if user.role == "client":
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

        await safe_edit_text(
            message,
            text,
            reply_markup=client_main_menu(),
        )
        return

    # =====================================================
    # OPERATOR
    # =====================================================
    if user.role == "operator":
        await safe_edit_text(
            message,
            "👨‍💼 <b>Панель оператора</b>",
            reply_markup=operator_main_menu(on_shift=False),
        )
        return

    # =====================================================
    # ADMIN
    # =====================================================
    if user.role == "admin":
        await safe_edit_text(
            message,
            "🛠 <b>Админ-панель</b>",
            reply_markup=admin_main_menu(),
        )
        return
