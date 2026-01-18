from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def chat_kb(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="💬 Написать сообщение",
                callback_data=f"chat:msg:{order_id}"
            ),
            InlineKeyboardButton(
                text="👑 Позвать админа",
                callback_data=f"chat:escalate:{order_id}"
            ),
        ]
    ])

