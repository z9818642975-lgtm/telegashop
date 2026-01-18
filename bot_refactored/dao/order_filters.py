from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot_refactored.models.order import Order, OrderStatus


class OrderFilterDAO:

    @staticmethod
    async def filter_orders(
        session: AsyncSession,
        *,
        status: OrderStatus | None = None,
        operator_id: int | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[Order]:

        stmt = select(Order)

        if status:
            stmt = stmt.where(Order.status == status)

        if operator_id:
            stmt = stmt.where(Order.operator_id == operator_id)

        if date_from:
            stmt = stmt.where(Order.created_at >= date_from)

        if date_to:
            stmt = stmt.where(Order.created_at <= date_to)

        res = await session.execute(stmt.order_by(Order.created_at.desc()))
        return res.scalars().all()

