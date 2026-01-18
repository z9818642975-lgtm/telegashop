from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def confirm_reject_kb(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="вњ… РџРѕРґС‚РІРµСЂРґРёС‚СЊ",
                    callback_data=f"confirm:{order_id}",
                ),
                InlineKeyboardButton(
                    text="вќЊ РћС‚РєР»РѕРЅРёС‚СЊ",
                    callback_data=f"reject:{order_id}",
                ),
            ]
        ]
    )

