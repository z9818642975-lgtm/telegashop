from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from bot_refactored.models.order_chat import OrderChatMessage
from bot_refactored.constants.roles import ADMINS

router = Router(name="admin_chats")

def _is_admin(client_id: int) -> bool:
    return client_id in ADMINS

@router.callback_query(F.data == "admin:chats")
async def chats(cb: CallbackQuery, session: AsyncSession):
    if not _is_admin(cb.from_user.id):
        return

    res = await session.execute(
        select(OrderChatMessage)
        .order_by(OrderChatMessage.created_at.desc())
        .limit(20)
    )
    messages = res.scalars().all()

    text = ["💬 Последние сообщения:"]
    for m in messages:
        text.append(
            f"[{m.created_at}] #{m.order_id} | {m.sender_id}: {m.text}"
        )

    await cb.message.edit_text("\n".join(text))

