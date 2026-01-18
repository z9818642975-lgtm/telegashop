from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def order_item_actions_kb(item_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="СЂСџвЂўвЂ™ 10 Р СР С‘Р Р…РЎС“РЎвЂљ",
                    callback_data=f"item:wait:{item_id}",
                ),
                InlineKeyboardButton(
                    text="РІСљвЂ¦ Р вЂ”Р В°Р В±РЎР‚Р В°Р В»",
                    callback_data=f"item:done:{item_id}",
                ),
            ]
        ]
    )

