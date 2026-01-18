from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot_refactored.services.chat_antispam import check_client_rate_limit
from bot_refactored.services.admin_chat_alert import notify_admin_chat_request
from bot_refactored.constants.roles import ADMINS

router = Router(name="chat")

@router.callback_query(F.data.startswith("chat:escalate:"))
async def escalate(cb: CallbackQuery):
    order_id = int(cb.data.split(":")[-1])
    for admin_id in ADMINS:
        await notify_admin_chat_request(
            cb.bot, admin_id, order_id, cb.from_user.id
        )
    await cb.answer("Администратор уведомлён")

@router.message(F.text)
async def chat_message(msg: Message, session: AsyncSession):
    # анти-спам для клиента
    if not check_client_rate_limit(msg.from_user.id):
        await msg.answer("⏱ Можно писать не чаще 1 сообщения в 10 секунд")
        return

    # здесь сохраняется сообщение в OrderChatMessage (у тебя уже есть модель)
    # и пересылается адресату (оператору/клиенту)
    await msg.answer("Сообщение отправлено")

