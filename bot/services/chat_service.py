from __future__ import annotations
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from bot.models.chat import Chat

class ChatService:
    def __init__(self, s: AsyncSession):
        self.s = s

    async def get_or_create(self, client_id: int, operator_id: int | None = None, order_id: int | None = None) -> Chat:
        q = select(Chat).where(Chat.client_id==client_id, Chat.is_active.is_(True))
        if order_id is not None:
            q = q.where(Chat.order_id==order_id)
        res = await self.s.execute(q)
        chat = res.scalar_one_or_none()
        if chat:
            return chat
        chat = Chat(client_id=client_id, operator_id=operator_id, order_id=order_id, is_active=True)
        self.s.add(chat); await self.s.flush()
        await self.s.commit()
        return chat

    async def request_admin(self, chat_id: int) -> bool:
        res = await self.s.execute(select(Chat).where(Chat.id==chat_id))
        chat = res.scalar_one()
        if chat.admin_requested_at:
            return False
        chat.admin_requested_at = datetime.utcnow()
        await self.s.commit()
        return True

    async def join_as_admin(self, chat_id: int, admin_id: int):
        res = await self.s.execute(select(Chat).where(Chat.id==chat_id))
        chat = res.scalar_one()
        chat.admin_id = admin_id
        chat.admin_joined_at = datetime.utcnow()
        await self.s.commit()
        return chat
