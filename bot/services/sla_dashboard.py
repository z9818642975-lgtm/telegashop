# bot/services/sla_dashboard.py
from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.enums import OrderStatus
from bot.models.order import Order


class SLADashboard:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def stats(self) -> dict:
        total = await self.session.scalar(
            select(func.count()).select_from(Order)
        )
        overdue = await self.session.scalar(
            select(func.count()).where(
                Order.sla_deadline.is_not(None),
                Order.sla_deadline < datetime.utcnow(),
            )
        )
        in_work = await self.session.scalar(
            select(func.count()).where(Order.status == OrderStatus.IN_WORK)
        )

        return {
            "total": total,
            "in_work": in_work,
            "overdue": overdue,
        }
