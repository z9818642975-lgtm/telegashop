from datetime import timedelta
from bot_refactored.services.notifications import notify

async def process_shift_sla(bot, shift, delta):
    if delta >= timedelta(minutes=15):
        await notify(bot, shift.operator_id, "⚠️ Вы неактивны 15 минут")
    if delta >= timedelta(minutes=17):
        await notify(bot, shift.operator_id, "⚠️ Вы неактивны 17 минут")
    if delta >= timedelta(minutes=18):
        await notify(bot, shift.operator_id, "❗ Вы неактивны 18 минут")
    if delta >= timedelta(minutes=20):
        await notify(bot, shift.operator_id, "⛔ Смена закрыта автоматически")

