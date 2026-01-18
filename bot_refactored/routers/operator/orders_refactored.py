from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.role import RoleFilter

from bot_refactored.app.orders.accept_order import AcceptOrderUseCase
from bot_refactored.app.orders.complete_order import CompleteOrderUseCase

router = Router(name="operator_orders_refactored")


@router.callback_query(RoleFilter("operator"), F.data.startswith("order:accept:"))
async def accept_order(cb: CallbackQuery, session: AsyncSession):
    order_id = int(cb.data.split(":")[-1])
    await AcceptOrderUseCase(
        order_id=order_id,
        operator_id=cb.from_user.id,
        session=session,
    ).execute()
    await cb.answer("Заказ принят")


@router.callback_query(RoleFilter("operator"), F.data.startswith("order:done:"))
async def complete_order(cb: CallbackQuery, session: AsyncSession):
    order_id = int(cb.data.split(":")[-1])
    await CompleteOrderUseCase(
        order_id=order_id,
        operator_id=cb.from_user.id,
        session=session,
    ).execute()
    await cb.answer("Заказ завершён")

