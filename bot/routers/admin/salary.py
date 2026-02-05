# bot/routers/admin/salary.py
from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.callbacks_common import AdminSalaryMenuCB, AdminSalaryPayCB
from bot.dao.salary_dao import SalaryDAO
from bot.filters.role import RoleFilter
from bot.keyboards.admin.salary import admin_salary_kb
from bot.models.enums import UserRole
from bot.services.notify_service import NotifyService

router = Router(name="admin_salary")
router.callback_query.filter(RoleFilter(UserRole.ADMIN))


@router.callback_query(AdminSalaryMenuCB.filter())
async def admin_salary_menu(
    cb: CallbackQuery,
    session: AsyncSession,
):
    dao = SalaryDAO(session)
    accruals = await dao.list_requested()

    await cb.message.edit_text(
        "💼 <b>Запросы на выплату</b>",
        reply_markup=admin_salary_kb(accruals),
    )
    await cb.answer()


@router.callback_query(AdminSalaryPayCB.filter())
async def admin_salary_pay(
    cb: CallbackQuery,
    callback_data: AdminSalaryPayCB,
    session: AsyncSession,
    bot,
):

    dao = SalaryDAO(session)

    accrual = await session.get(
        dao.model, callback_data.accrual_id
    )

    if not accrual:
        await cb.answer("Начисление не найдено", show_alert=True)
        return

    await dao.mark_paid([accrual.id])
    await session.commit()

    notify = NotifyService(bot, session)
    await notify.notify_client(
        accrual.operator.tg_id,
        "💸 Ваша выплата подтверждена и помечена как PAID",
    )

    await cb.answer("Выплата подтверждена")