# bot/keyboards/client/pickup_actions.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def pickup_actions_kb(order_item_id: int) -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🕒 10 минут",
                    callback_data=f"pickup:wait:{order_item_id}",
                ),
                InlineKeyboardButton(


                    text="✅ Забрал",
                    callback_data=f"pickup:done:{order_item_id}",
                ),
            ]
        ]
    )





