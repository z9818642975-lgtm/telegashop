from __future__ import annotations

import asyncio
from aiogram import Bot

from bot.config import settings
from bot.db import async_session_maker
from bot.dao.orders_dao import OrdersDAO
from bot.models.enums import OrderStatus


def start_pickup_timer(order_id: int) -> None:
    asyncio.create_task(_pickup_timer(order_id))


async def _pickup_timer(order_id: int) -> None:
    # ждём 8 минут
    await asyncio.sleep(8 * 60)

    async with async_session_maker() as session:
        dao = OrdersDAO(session)
        order = await dao.get(order_id)

        if not order:
            return

        if order.status != OrderStatus.READY:
            return

        if order.pickup_notified:
            return

        if not order.pickup_photo_id:
            return

        bot = Bot(token=settings.BOT_TOKEN)

        try:
            await bot.send_photo(
                chat_id=order.client_id,
                photo=order.pickup_photo_id,
                caption=order.pickup_comment or "📦 Заказ готов к самовывозу",
            )

            order.pickup_notified = True
            await session.commit()

        finally:
            await bot.session.close()

