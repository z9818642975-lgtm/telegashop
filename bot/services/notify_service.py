# bot/services/notify_service.py
# bot/services/notify_service.py
from __future__ import annotations

from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncSession

from bot.dao.operators_dao import OperatorsDAO


class NotifyService:


    def __init__(self, bot: Bot, session: AsyncSession):


        self.bot = bot


        self.session = session





    async def notify_operators(self, text: str, reply_markup=None, photo_id: str | None = None, document_id: str | None = None):


        dao = OperatorsDAO(self.session)


        operators = await dao.list_active()


        for op in operators:


            try:


                await self.bot.send_message(op.tg_id, text, reply_markup=reply_markup)


                if document_id:


                    await self.bot.send_document(op.tg_id, document_id)


                if photo_id:


                    await self.bot.send_photo(op.tg_id, photo_id)


            except Exception:


                # do not crash main flow


                pass





    async def notify_client(self, client_id: int, text: str):


        try:


            await self.bot.send_message(client_id, text)


        except Exception:


            pass







