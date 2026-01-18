# bot/services/order_workflow.py
import asyncio

from bot.db import async_session_maker
from bot.dao.orders_dao import OrdersDAO


def schedule_assembling(order_id: int, delay: int = 10) -> None:
    async def task():
        await asyncio.sleep(delay)
        async with async_session_maker() as session:
            await OrdersDAO(session).mark_assembling(order_id)
            await session.commit()

    asyncio.create_task(task())

