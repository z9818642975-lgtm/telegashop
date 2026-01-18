from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.order import Order
from bot.constants.order_status import OrderStatus
from bot.services.inventory import InventoryService
from bot.services.notifications import NotificationService
from bot.config import settings

router = Router(name="operator_confirm")

@router.callback_query(F.data.startswith("operator:confirm:"))
async def confirm_order(
    cb: CallbackQuery,
    *,
    session: AsyncSession | None = None,
    bot,
):
    order_id = int(cb.data.split(":")[1])
    order = await session.get(Order, order_id)

    await InventoryService.deduct(session, order.id)
    order.status = OrderStatus.PAID

    await NotificationService.notify_client(
        bot,
        order.client_id,
        "РІСљвЂ¦ Р вЂ™Р В°РЎв‚¬ Р В·Р В°Р С”Р В°Р В· Р С—Р С•Р Т‘РЎвЂљР Р†Р ВµРЎР‚Р В¶Р Т‘РЎвЂР Р… Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚Р С•Р С.",
    )

    await NotificationService.notify_admin(
        bot,
        list(settings.ADMINS)[0],
        f"СЂСџвЂњВ¦ Р вЂ”Р В°Р С”Р В°Р В· #{order.id} Р С—Р С•Р Т‘РЎвЂљР Р†Р ВµРЎР‚Р В¶Р Т‘РЎвЂР Р…",
    )

    await cb.message.answer(f"РІСљвЂ¦ Р вЂ”Р В°Р С”Р В°Р В· #{order.id} Р С—Р С•Р Т‘РЎвЂљР Р†Р ВµРЎР‚Р В¶Р Т‘РЎвЂР Р…")
    await cb.answer()

@router.callback_query(F.data.startswith("operator:reject:"))
async def reject_order(
    cb: CallbackQuery,
    *,
    session: AsyncSession | None = None,
    bot,
):
    order_id = int(cb.data.split(":")[1])
    order = await session.get(Order, order_id)

    order.status = OrderStatus.REJECTED

    await NotificationService.notify_client(
        bot,
        order.client_id,
        "РІСњРЉ Р вЂ”Р В°Р С”Р В°Р В· Р С•РЎвЂљР С”Р В»Р С•Р Р…РЎвЂР Р…. Р СџРЎР‚Р С•Р Р†Р ВµРЎР‚РЎРЉРЎвЂљР Вµ РЎвЂЎР ВµР С” Р С‘ Р С—Р С•Р С—РЎР‚Р С•Р В±РЎС“Р в„–РЎвЂљР Вµ РЎРѓР Р…Р С•Р Р†Р В°.",
    )

    await cb.message.answer(f"РІСњРЉ Р вЂ”Р В°Р С”Р В°Р В· #{order.id} Р С•РЎвЂљР С”Р В»Р С•Р Р…РЎвЂР Р…")
    await cb.answer()


