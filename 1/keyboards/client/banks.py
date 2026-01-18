# bot/keyboards/client/banks.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def banks_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="РЎР‚РЎСџР РЏР’В¦ Р В Р Р‹Р В Р’В±Р В Р’ВµР РЋР вЂљ",
                    callback_data="client:bank:sber",
                ),
                InlineKeyboardButton(
                    text="РЎР‚РЎСџР РЏР’В¦ Р В РЎС›-Р В РІР‚ВР В Р’В°Р В Р вЂ¦Р В РЎвЂќ",
                    callback_data="client:bank:tinkoff",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="РЎР‚РЎСџР РЏР’В¦ Р В РЎвЂ™Р В Р’В»Р РЋР Р‰Р РЋРІР‚С›Р В Р’В°",
                    callback_data="client:bank:alfa",
                ),
                InlineKeyboardButton(
                    text="Р Р†РЎв„ўР Р‹ Р В Р Р‹Р В РІР‚ВР В РЎСџ",
                    callback_data="client:bank:sbp",
                ),
            ],
        ]
    )

