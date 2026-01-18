from aiogram import Bot
from bot_refactored.constants.roles import ADMINS


async def notify_operator_sla(bot: Bot, operator_id: int, order_id: int):
    await bot.send_message(
        operator_id,
        f"⏱ SLA: нет ответа клиенту по заказу #{order_id}"
    )


async def notify_admin_sla(bot: Bot, order_id: int):
    for admin_id in ADMINS:
        await bot.send_message(
            admin_id,
            f"⛔ SLA: оператор не ответил по заказу #{order_id}"
        )

