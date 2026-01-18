from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.services.salary import SalaryService

router = Router(name="operator_salary")

@router.callback_query(F.data.startswith("operator:confirm:"))
async def accrue_salary(
    cb: CallbackQuery,
    *,
    session: AsyncSession | None = None,
):
    order_id = int(cb.data.split(":")[1])
    operator_id = cb.from_user.id
    await SalaryService.accrue(
        session=session,
        operator_id=operator_id,
        order_id=order_id,
        amount=100,  # РЎвЂћР С‘Р С”РЎРѓ Р В·Р В° Р В·Р В°Р С”Р В°Р В·
    )


