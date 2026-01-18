from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.constants.callbacks import CB


def profile_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="РЎР‚РЎСџРІР‚СљР’В¦ Р В РЎС™Р В РЎвЂўР В РЎвЂ Р В Р’В·Р В Р’В°Р В РЎвЂќР В Р’В°Р В Р’В·Р РЋРІР‚в„–",
                    callback_data="client:profile:orders",
                ),
                InlineKeyboardButton(
                    text="РЎР‚РЎСџРІР‚ВРўС’ Р В Р’В Р В Р’ВµР РЋРІР‚С›Р В Р’ВµР РЋР вЂљР В Р’В°Р В Р’В»Р РЋРІР‚в„–",
                    callback_data="client:profile:ref",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="РЎР‚РЎСџР вЂ№РЎСџ Р В РЎв„ўР РЋРЎвЂњР В РЎвЂ”Р В РЎвЂўР В Р вЂ¦",
                    callback_data="client:profile:coupon",
                ),
                InlineKeyboardButton(
                    text="Р Р†Р’В¬РІР‚В¦Р С—РЎвЂР РЏ Р В РЎСљР В Р’В°Р В Р’В·Р В Р’В°Р В РўвЂ",
                    callback_data=CB.BACK_MENU,
                ),
            ],
        ]
    )

