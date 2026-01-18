# bot/keyboards/client/pickup_actions.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def pickup_actions_kb(order_item_id: int) -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="СЂСџвЂўвЂ™ 10 Р СР С‘Р Р…РЎС“РЎвЂљ",
                    callback_data=f"pickup:wait:{order_item_id}",
                ),
                InlineKeyboardButton(


                    text="РІСљвЂ¦ Р вЂ”Р В°Р В±РЎР‚Р В°Р В»",
                    callback_data=f"pickup:done:{order_item_id}",
                ),
            ]
        ]
    )





