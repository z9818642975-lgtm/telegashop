
from bot.actions.operator import OperatorAction
from bot.routers.operator.action_dispatcher import register


@register(OperatorAction.SHIFT_START)
async def shift_start(cb, callback_data, session, user, state):
    await cb.answer("▶️ Смена начата")


@register(OperatorAction.SHIFT_STOP)
async def shift_stop(cb, callback_data, session, user, state):
    await cb.answer("⏹ Смена завершена")


@register(OperatorAction.ORDERS_ACTIVE)
async def orders_active(cb, callback_data, session, user, state):
    await cb.answer("📦 Активные заказы")