from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot_refactored.models.order import Order, OrderStatus


SLA_HOURS = 2  # можно менять


async def get_expired_payment_orders(session: AsyncSession):
    deadline = datetime.utcnow() - timedelta(hours=SLA_HOURS)

    stmt = select(Order).where(
        Order.status == OrderStatus.WAITING_CONFIRMATION,
        Order.created_at <= deadline,
    )

    result = await session.execute(stmt)
    return result.scalars().all()

