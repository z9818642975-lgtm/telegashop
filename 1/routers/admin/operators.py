from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.role import RoleFilter
from bot.dao.users_dao import UsersDAO
from bot.keyboards.admin.operators import operators_kb

router = Router(name="admin_operators")

@router.callback_query(RoleFilter("admin"), F.data == "admin:operators")
async def operators_list(cb, *, session: AsyncSession | None = None):
    dao = UsersDAO(session)
    operators = await dao.list_operators()
    await cb.message.edit_text("Р РЋР вЂљР РЋРЎСџР Р†Р вЂљР’ВР вЂ™Р’В· Р В Р’В Р РЋРІР‚С”Р В Р’В Р РЋРІР‚вЂќР В Р’В Р вЂ™Р’ВµР В Р Р‹Р В РІР‚С™Р В Р’В Р вЂ™Р’В°Р В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р РЋРІР‚СћР В Р Р‹Р В РІР‚С™Р В Р Р‹Р Р†Р вЂљРІвЂћвЂ“", reply_markup=operators_kb(operators))
    await cb.answer()

@router.callback_query(RoleFilter("admin"), F.data.startswith("admin:operator:toggle"))
async def operator_toggle(cb, *, session: AsyncSession | None = None):
    operator_id = int(cb.data.split(":")[-1])
    dao = UsersDAO(session)
    await dao.toggle_active(operator_id)
    await session.commit()
    operators = await dao.list_operators()
    await cb.message.edit_reply_markup(reply_markup=operators_kb(operators))
    await cb.answer("OK")



