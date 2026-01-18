from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.constants.callbacks import CB


def delivery_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="СЂСџвЂњРЊ Р РЋР В°Р СР С•Р Р†РЎвЂ№Р Р†Р С•Р В·",
                    callback_data=CB.DELIVERY_PICKUP,
                ),
                InlineKeyboardButton(
                    text="СЂСџС™С™ Р С™РЎС“РЎР‚РЎРЉР ВµРЎР‚",
                    callback_data=CB.DELIVERY_COURIER,
                ),
            ],
            [
                InlineKeyboardButton(
                    text="РІВ¬вЂ¦РїС‘РЏ Р вЂ™ Р С”Р С•РЎР‚Р В·Р С‘Р Р…РЎС“",
                    callback_data=CB.CART_OPEN,
                )
            ],
        ]
    )

