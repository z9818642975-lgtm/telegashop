from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot_refactored.models.order import Order, OrderStatus


class OrdersDAO:

    @staticmethod
    async def get_for_update(
        session: AsyncSession,
        order_id: int,
    ) -> Order | None:
        stmt = (
            select(Order)
            .where(Order.id == order_id)
            .with_for_update()
        )
        res = await session.execute(stmt)
        return res.scalar_one_or_none()

    @staticmethod
    async def accept(
        order: Order,
        operator_id: int,
        shift_id: int,
    ) -> None:
        order.operator_id = operator_id
        order.shift_id = shift_id
        order.status = OrderStatus.ACCEPTED

    @staticmethod
    async def mark_paid(order: Order) -> None:
        order.status = OrderStatus.PAID
        order.paid_at = datetime.utcnow()

    @staticmethod
    async def complete(order: Order) -> None:
        order.status = OrderStatus.DONE
        order.completed_at = datetime.utcnow()

