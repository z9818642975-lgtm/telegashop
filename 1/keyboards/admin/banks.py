from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def banks_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Р РЋР вЂљР РЋРЎСџР Р†Р вЂљРЎС™Р Р†Р вЂљРЎвЂє Р В Р’В Р В Р вЂ№Р В Р’В Р РЋРІР‚вЂќР В Р’В Р РЋРІР‚ВР В Р Р‹Р В РЎвЂњР В Р’В Р РЋРІР‚СћР В Р’В Р РЋРІР‚Сњ Р В Р’В Р вЂ™Р’В±Р В Р’В Р вЂ™Р’В°Р В Р’В Р В РІР‚В¦Р В Р’В Р РЋРІР‚СњР В Р’В Р РЋРІР‚СћР В Р’В Р В РІР‚В ",
                    callback_data="admin:bank:list",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Р В Р вЂ Р РЋРІР‚С”Р Р†Р вЂљРЎС› Р В Р’В Р Р†Р вЂљРЎСљР В Р’В Р РЋРІР‚СћР В Р’В Р вЂ™Р’В±Р В Р’В Р вЂ™Р’В°Р В Р’В Р В РІР‚В Р В Р’В Р РЋРІР‚ВР В Р Р‹Р Р†Р вЂљРЎв„ўР В Р Р‹Р В Р вЂ° Р В Р’В Р вЂ™Р’В±Р В Р’В Р вЂ™Р’В°Р В Р’В Р В РІР‚В¦Р В Р’В Р РЋРІР‚Сњ",
                    callback_data="admin:bank:create",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Р В Р вЂ Р вЂ™Р’В¬Р Р†Р вЂљР’В¦Р В РЎвЂ”Р РЋРІР‚ВР В Р РЏ Р В Р’В Р РЋРЎС™Р В Р’В Р вЂ™Р’В°Р В Р’В Р вЂ™Р’В·Р В Р’В Р вЂ™Р’В°Р В Р’В Р СћРІР‚В",
                    callback_data="admin:panel",
                ),
            ],
        ]
    )

