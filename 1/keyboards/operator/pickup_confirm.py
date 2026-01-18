from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def pickup_confirm_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Р Р†РЎС™РІР‚В¦ Р В РЎСџР В РЎвЂўР В РўвЂР РЋРІР‚С™Р В Р вЂ Р В Р’ВµР РЋР вЂљР В РўвЂР В РЎвЂР РЋРІР‚С™Р РЋР Р‰",
                    callback_data="operator:op:pickup:confirm",
                ),
                InlineKeyboardButton(
                    text="Р Р†РЎСљР Р‰ Р В РЎвЂєР РЋРІР‚С™Р В РЎВР В Р’ВµР В Р вЂ¦Р В РЎвЂР РЋРІР‚С™Р РЋР Р‰",
                    callback_data="operator:op:pickup:cancel",
                ),
            ]
        ]
    )

