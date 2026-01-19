from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def pickup_confirm_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Подтвердить",
                    callback_data="operator:pickup:confirm",
                ),
                InlineKeyboardButton(
                    text="❌ Отменить",
                    callback_data="operator:pickup:cancel",
                ),
            ]
        ]
    )

