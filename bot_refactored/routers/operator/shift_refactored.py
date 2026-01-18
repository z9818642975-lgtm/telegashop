from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.role import RoleFilter

from bot_refactored.app.operator_shift.open_shift import OpenShiftUseCase
from bot_refactored.app.operator_shift.close_shift import CloseShiftUseCase

router = Router(name="operator_shift_refactored")


@router.callback_query(RoleFilter("operator"), F.data == "shift:open")
async def open_shift(cb: CallbackQuery, session: AsyncSession):
    await OpenShiftUseCase(
        operator_id=cb.from_user.id,
        pickup_address="ADDRESS_FROM_FSM",  # временно, позже подключим FSM
        session=session,
    ).execute()
    await cb.answer("Смена открыта")


@router.callback_query(RoleFilter("operator"), F.data == "shift:close")
async def close_shift(cb: CallbackQuery, session: AsyncSession):
    await CloseShiftUseCase(
        operator_id=cb.from_user.id,
        session=session,
    ).execute()
    await cb.answer("Смена закрыта")

