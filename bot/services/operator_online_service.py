from __future__ import annotations
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from bot.dao.users_dao import UsersDAO
from bot.dao.shifts_dao import ShiftsDAO
from bot.dao.orders_dao import OrdersDAO
from bot.models.order import Order
from bot.models.enums import OrderStatus
from bot.services.admin_notify_service import AdminNotifyService

class OperatorOnlineService:
    def __init__(self, s: AsyncSession):
        self.s = s
        self.users = UsersDAO(s)
        self.shifts = ShiftsDAO(s)
        self.orders = OrdersDAO(s)
        self.notify = AdminNotifyService()

    async def check_operator(self, operator_tg_id: int, bot=None):
        user = await self.users.get_by_tg(operator_tg_id)
        shift = await self.shifts.get_active(operator_tg_id)
        if not user or not shift or not user.last_seen_at:
            return

        now = datetime.utcnow()
        delta = now - user.last_seen_at

        if timedelta(minutes=10) <= delta < timedelta(minutes=12):
            if bot: await self.notify.operator_offline(bot, operator_tg_id, 1)
        elif timedelta(minutes=12) <= delta < timedelta(minutes=14):
            if bot: await self.notify.operator_offline(bot, operator_tg_id, 2)
        elif timedelta(minutes=14) <= delta < timedelta(minutes=15):
            if bot: await self.notify.operator_offline(bot, operator_tg_id, 3)
        elif delta >= timedelta(minutes=15):
            await self.shifts.close_active(operator_tg_id, auto_closed=True)
            await self.s.commit()
            if bot: await self.notify.shift_auto_closed(bot, operator_tg_id)

    async def list_active_operators(self):
        return await self.users.list_operators_with_active_shift()
