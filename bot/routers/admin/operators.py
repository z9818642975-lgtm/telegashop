from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.role import RoleFilter
from bot.dao.users_dao import UsersDAO
from bot.keyboards.admin.operators import operators_kb

router = Router(name="admin_operators")

@router.callback_query(RoleFilter("admin"), F.data == "admin:operators")
async def operators_list(cb: CallbackQuery, session: AsyncSession):
    dao = UsersDAO(session)
    operators = await dao.list_operators()
    await cb.message.edit_text("👷 Операторы", reply_markup=operators_kb(operators))
    await cb.answer()

@router.callback_query(RoleFilter("admin"), F.data.startswith("admin:operator:toggle"))
async def operator_toggle(cb: CallbackQuery, session: AsyncSession):
    operator_id = int(cb.data.split(":")[-1])
    dao = UsersDAO(session)
    await dao.toggle_active(operator_id)
    await session.commit()
    operators = await dao.list_operators()
    await cb.message.edit_reply_markup(reply_markup=operators_kb(operators))
    await cb.answer("OK")

