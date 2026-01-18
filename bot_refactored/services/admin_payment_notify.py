from aiogram import Bot

async def notify_admin_payment(
    bot: Bot,
    admin_id: int,
    order_id: int,
    operator_id: int,
):
    await bot.send_message(
        admin_id,
        f"💰 Заказ #{order_id} оплачен\nОператор {operator_id}"
    )

