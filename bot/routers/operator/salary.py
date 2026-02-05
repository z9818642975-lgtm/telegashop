# bot/routers/operator/salary.py
from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.callbacks_common import OperatorSalaryPayoutCB, OperatorSalaryStatsCB
from bot.dao.salary_dao import SalaryDAO
from bot.filters.role import RoleFilter
from bot.keyboards.operator.salary import operator_salary_menu_kb
from bot.models.enums import UserRole
from bot.models.user import User

router = Router(name="operator_salary")
router.callback_query.filter(RoleFilter(UserRole.OPERATOR))


@router.callback_query(OperatorSalaryStatsCB.filter())
async def operator_salary_stats(
    cb: CallbackQuery,
    callback_data: OperatorSalaryStatsCB,
    session: AsyncSession,
    user: User,
):
    dao = SalaryDAO(session)
    stats = await dao.get_stats(
        operator_id=user.id,
        period=callback_data.period,
    )

    await cb.message.edit_text(
        f"📊 <b>Статистика ({callback_data.period})</b>\n\n"
        f"📦 Заказов: <b>{stats['orders']}</b>\n"
        f"💰 Сумма: <b>{stats['amount']} ₽</b>",
        reply_markup=operator_salary_menu_kb(),
    )
    await cb.answer()


@router.callback_query(OperatorSalaryPayoutCB.filter())
async def operator_salary_payout(
    cb: CallbackQuery,
    session: AsyncSession,
    user: User,
):
    dao = SalaryDAO(session)
    await dao.request_payout(operator_id=user.id)
    await session.commit()

    await cb.message.edit_text(
        "💸 Запрос на выплату отправлен администратору",
        reply_markup=operator_salary_menu_kb(),
    )
    await cb.answer()