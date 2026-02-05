# bot/services/sla_watcher.py
import asyncio

from aiogram import Bot

from bot.dao.orders_dao import OrdersDAO
from bot.db.session import async_session
from bot.models.enums import OrderStatus
from bot.services.notifier import Notifier


async def sla_watcher(bot: Bot):
    notifier = Notifier()

    while True:
        async with async_session() as session:
            orders = await OrdersDAO(session).get_sla_expired()

            for order in orders:
                if getattr(order, "assigned_operator_tg_id", None):
                    await notifier.operator(
                        bot,
                        order.assigned_operator_tg_id,
                        f"❌ SLA: заказ #{order.id} снят и возвращён в очередь",
                    )

                order.assigned_operator_id = None
                order.sla_deadline = None
                order.status = OrderStatus.PAID

            if orders:
                await session.commit()

        await asyncio.sleep(30)

