# bot/services/auto_done.py
import asyncio
from bot.db import async_session_maker
from bot.dao.orders_dao import OrdersDAO
from bot.models.enums import OrderStatus

_running_done: set[int] = set()


def start_auto_done(order_id: int, delay_minutes: int = 20):
    if order_id in _running_done:
        return
    _running_done.add(order_id)
    asyncio.create_task(_auto_done(order_id, delay_minutes))


async def _auto_done(order_id: int, delay_minutes: int):
    await asyncio.sleep(delay_minutes * 60)

    async with async_session_maker() as session:
        order = await OrdersDAO(session).get(order_id)
        if not order or order.status != OrderStatus.READY:
            _running_done.discard(order_id)
            return

        order.status = OrderStatus.DONE
        await session.commit()

    _running_done.discard(order_id)

