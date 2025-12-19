from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from bot.dao.orders_dao import OrdersDAO
from bot.dao.shifts_dao import ShiftsDAO
from bot.models.enums import OrderStatus
from bot.services.stock_service import StockService
from bot.services.admin_notify_service import AdminNotifyService

class OrderService:
    def __init__(self, s: AsyncSession):
        self.s = s
        self.orders = OrdersDAO(s)
        self.shifts = ShiftsDAO(s)
        self.stock = StockService(s)
        self.notify = AdminNotifyService()

    async def create_order(self, client_tg_id: int, delivery_method: str):
        order = await self.orders.create(client_id=client_tg_id, status=OrderStatus.WAIT_PAYMENT.value, delivery_method=delivery_method, delivery_fee=0)
        await self.s.commit()
        return order

    async def set_courier_fee(self, order_id: int, fee: int):
        await self.orders.set_delivery(order_id, method="COURIER", fee=fee)
        await self.s.commit()

    async def set_pickup_point(self, order_id: int, shift_id: int, operator_tg_id: int, address: str):
        await self.orders.set_delivery(order_id, method="PICKUP", fee=0, shift_id=shift_id, operator_id=operator_tg_id, pickup_addr=address)
        await self.s.commit()

    async def auto_reassign_pickup(self, order_id: int, new_shift_id: int, new_operator_tg_id: int, new_addr: str, bot=None):
        await self.orders.reassign_pickup(order_id, new_operator_tg_id, new_shift_id, new_addr)
        await self.stock.move_reservation(order_id, new_operator_tg_id)
        await self.s.commit()
        if bot:
            await self.notify.pickup_reassigned(bot, order_id, new_operator_tg_id, new_addr)
