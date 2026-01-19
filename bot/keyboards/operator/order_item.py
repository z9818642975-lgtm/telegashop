from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def order_item_actions_kb(item_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🕒 10 минут",
                    callback_data=f"client:item:wait:{item_id}",
                ),
                InlineKeyboardButton(
                    text="✅ Забрал",
                    callback_data=f"client:item:done:{item_id}",
                ),
            ]
        ]
    )

