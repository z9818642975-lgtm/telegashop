# bot/routers/client/payment.py

from aiogram import F, Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.dao.orders_dao import OrdersDAO
from bot.models.enums import OrderStatus

router = Router(name="client_payment")

@router.message(F.photo | F.document)
async def client_upload_payment_proof(
    msg: Message,
    session: AsyncSession,
):
    order = await OrdersDAO(session).get_active_order(msg.from_user.id)
    if not order:
        await msg.answer("❌ У вас нет активного заказа")
        return

    if msg.photo:
        file_id = msg.photo[-1].file_id
        file_type = "photo"
    else:
        file_id = msg.document.file_id
        file_type = "pdf"

    await OrdersDAO(session).save_payment_proof(
        order_id=order.id,
        file_id=file_id,
        file_type=file_type,
    )

    await OrdersDAO(session).set_status(
        order.id, OrderStatus.PAYMENT_CHECK
    )

    await msg.answer(
        "✅ Чек получен.\n"
        "Ожидайте подтверждения оператором."
    )
