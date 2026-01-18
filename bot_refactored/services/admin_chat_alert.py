from aiogram import Bot

async def notify_admin_chat_request(
    bot: Bot,
    admin_id: int,
    order_id: int,
    from_user: int,
):
    await bot.send_message(
        admin_id,
        f"👑 Запрос администратора\nЗаказ #{order_id}\nПользователь {from_user}"
    )

