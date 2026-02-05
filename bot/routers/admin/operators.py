# bot/routers/admin/operators.py
from aiogram import Router
from aiogram.types import CallbackQuery

from bot.constants.callbacks_admin import AdminOperatorToggle
from bot.dao.users_dao import UsersDAO

router = Router(name="admin_operators")


@router.callback_query(AdminOperatorToggle.filter())
async def operator_toggle(cb: CallbackQuery, callback_data: AdminOperatorToggle):
    dao = UsersDAO()
    await dao.toggle_active(callback_data.operator_id)

    await cb.answer("OK")

