from __future__ import annotations
from aiogram import Bot
from bot.core.config import settings
from bot.core.logger import logger

class AdminNotifyService:
    async def _send(self, bot: Bot, text: str):
        for admin in settings.ADMINS:
            try:
                await bot.send_message(admin, text)
            except Exception as e:
                logger.warning("Admin notify failed: %s", e)

    async def notify_new_order(self, bot: Bot, order_id: int, delivery_method: str):
        await self._send(bot, f"📦 Новый заказ #{order_id}\nСпособ: {delivery_method}")

    async def notify_admin_request(self, bot: Bot, chat_id: int):
        await self._send(bot, f"📣 Вызов админа в чат #{chat_id}\nКоманда: /join_chat {chat_id}")

    async def low_stock(self, bot: Bot, product_title: str, qty: int, warehouse_title: str):
        await self._send(bot, f"⚠️ Минимальный остаток\n{product_title}: {qty} шт\nСклад: {warehouse_title}")

    async def operator_offline(self, bot: Bot, operator_tg_id: int, level: int):
        await self._send(bot, f"⚠️ Оператор оффлайн L{level}: {operator_tg_id}")

    async def shift_auto_closed(self, bot: Bot, operator_tg_id: int):
        await self._send(bot, f"⛔ Смена закрыта автоматически: {operator_tg_id}")

    async def pickup_reassigned(self, bot: Bot, order_id: int, new_operator: int, addr: str):
        await self._send(bot, f"🔁 Самовывоз переназначен\nЗаказ #{order_id}\nОператор: {new_operator}\nАдрес: {addr}")

    async def no_operator(self, bot: Bot, order_id: int):
        await self._send(bot, f"⛔ Нет онлайн оператора для самовывоза\nЗаказ #{order_id}")
