# bot/services/operator_queue_service.py
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.enums import OrderStatus
from bot.models.operator_shift import OperatorShift
from bot.models.order import Order


class OperatorQueueService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def assign_next_operator(self, order: Order) -> bool:
        stmt = (
            select(OperatorShift)
            .where(OperatorShift.ended_at.is_(None))
            .order_by(OperatorShift.started_at.asc())
            .limit(1)
        )
        shift = await self.session.scalar(stmt)
        if not shift:
            return False

        order.assigned_operator_id = shift.operator_id
        order.assigned_operator_tg_id = shift.operator.tg_id
        order.status = OrderStatus.IN_WORK
        order.sla_deadline = datetime.utcnow() + timedelta(minutes=order.sla_minutes)

        await self.session.flush()
        return True