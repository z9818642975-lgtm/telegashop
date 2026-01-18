from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot_refactored.keyboards.admin import admin_main_kb, operators_kb
from bot_refactored.dao.operators import OperatorsDAO
from bot_refactored.constants.roles import ADMINS

router = Router(name="admin_panel")

PAGE_SIZE = 5

def _is_admin(client_id: int) -> bool:
    return client_id in ADMINS

@router.callback_query(F.data == "admin:panel")
async def admin_panel(cb: CallbackQuery):
    if not _is_admin(cb.from_user.id):
        return
    await cb.message.edit_text("👑 Админ-панель", reply_markup=admin_main_kb())

@router.callback_query(F.data.startswith("admin:operators"))
async def operators(cb: CallbackQuery, session: AsyncSession):
    if not _is_admin(cb.from_user.id):
        return

    page = int(cb.data.split(":")[2]) if ":" in cb.data else 1
    ops = await OperatorsDAO.list_all(session)

    total = len(ops)
    pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE

    await cb.message.edit_text(
        "👷 Операторы:",
        reply_markup=operators_kb(ops[start:end], page, pages)
    )

