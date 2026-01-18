# bot/services/admin_notify_service.py
from __future__ import annotations

# bot/services/admin_notify_service.py
from __future__ import annotations


from aiogram import Bot


from bot.config import settings


from bot.core.logger import logger





class AdminNotifyService:


    async def _send(self, bot: Bot, text: str):


        for admin in settings.ADMINS:


            try:


                await bot.send_message(admin, text)


            except Exception as e:


                logger.warning("Admin notify failed: %s", e)





    async def notify_new_order(self, bot: Bot, order_id: int, delivery_method: str):


        await self._send(bot, f"СЂСџвЂњВ¦ Р СњР С•Р Р†РЎвЂ№Р в„– Р В·Р В°Р С”Р В°Р В· #{order_id}\nР РЋР С—Р С•РЎРѓР С•Р В±: {delivery_method}")





    async def notify_admin_request(self, bot: Bot, chat_id: int):


        await self._send(bot, f"СЂСџвЂњР€ Р вЂ™РЎвЂ№Р В·Р С•Р Р† Р В°Р Т‘Р СР С‘Р Р…Р В° Р Р† РЎвЂЎР В°РЎвЂљ #{chat_id}\nР С™Р С•Р СР В°Р Р…Р Т‘Р В°: /join_chat {chat_id}")





    async def low_stock(self, bot: Bot, product_title: str, qty: int, warehouse_title: str):


        await self._send(bot, f"РІС™В РїС‘РЏ Р СљР С‘Р Р…Р С‘Р СР В°Р В»РЎРЉР Р…РЎвЂ№Р в„– Р С•РЎРѓРЎвЂљР В°РЎвЂљР С•Р С”\n{product_title}: {qty} РЎв‚¬РЎвЂљ\nР РЋР С”Р В»Р В°Р Т‘: {warehouse_title}")





    async def operator_offline(self, bot: Bot, operator_tg_id: int, level: int):


        await self._send(bot, f"РІС™В РїС‘РЏ Р С›Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚ Р С•РЎвЂћРЎвЂћР В»Р В°Р в„–Р Р… L{level}: {operator_tg_id}")





    async def shift_auto_closed(self, bot: Bot, operator_tg_id: int):


        await self._send(bot, f"РІвЂєвЂќ Р РЋР СР ВµР Р…Р В° Р В·Р В°Р С”РЎР‚РЎвЂ№РЎвЂљР В° Р В°Р Р†РЎвЂљР С•Р СР В°РЎвЂљР С‘РЎвЂЎР ВµРЎРѓР С”Р С‘: {operator_tg_id}")





    async def pickup_reassigned(self, bot: Bot, order_id: int, new_operator: int, addr: str):


        await self._send(bot, f"СЂСџвЂќРѓ Р РЋР В°Р СР С•Р Р†РЎвЂ№Р Р†Р С•Р В· Р С—Р ВµРЎР‚Р ВµР Р…Р В°Р В·Р Р…Р В°РЎвЂЎР ВµР Р…\nР вЂ”Р В°Р С”Р В°Р В· #{order_id}\nР С›Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚: {new_operator}\nР С’Р Т‘РЎР‚Р ВµРЎРѓ: {addr}")





    async def no_operator(self, bot: Bot, order_id: int):


        await self._send(bot, f"РІвЂєвЂќ Р СњР ВµРЎвЂљ Р С•Р Р…Р В»Р В°Р в„–Р Р… Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚Р В° Р Т‘Р В»РЎРЏ РЎРѓР В°Р СР С•Р Р†РЎвЂ№Р Р†Р С•Р В·Р В°\nР вЂ”Р В°Р С”Р В°Р В· #{order_id}")





