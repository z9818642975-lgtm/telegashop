from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from bot.dao.shifts_dao import ShiftsDAO
from bot.dao.orders_dao import OrdersDAO
from bot.models.enums import OrderStatus

class OperatorService:
    def __init__(self, s: AsyncSession):
        self.s = s
        self.shifts = ShiftsDAO(s)
        self.orders = OrdersDAO(s)

    async def start_shift(self, operator_tg_id: int, address: str):
        await self.shifts.close_active(operator_tg_id, auto_closed=False)
        shift = await self.shifts.create(operator_tg_id, address)
        await self.s.commit()
        return shift

    async def end_shift(self, operator_tg_id: int):
        await self.shifts.close_active(operator_tg_id, auto_closed=False)
        await self.s.commit()

    async def take_to_work(self, order_id: int):
        await self.orders.set_status(order_id, OrderStatus.IN_PROGRESS.value)
        await self.s.commit()

    async def finish_order(self, order_id: int):
        await self.orders.set_status(order_id, OrderStatus.DONE.value)
        await self.s.commit()
