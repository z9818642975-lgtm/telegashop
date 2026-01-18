from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def admin_panel_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Р РЋР вЂљР РЋРЎСџР В Р РЏР вЂ™Р’В¬ Р В Р’В Р В Р вЂ№Р В Р’В Р РЋРІР‚СњР В Р’В Р вЂ™Р’В»Р В Р’В Р вЂ™Р’В°Р В Р’В Р СћРІР‚ВР В Р Р‹Р Р†Р вЂљРІвЂћвЂ“",
                    callback_data="admin:warehouses",
                ),
                InlineKeyboardButton(
                    text="Р РЋР вЂљР РЋРЎСџР Р†Р вЂљРЎС™Р вЂ™Р’В¦ Р В Р’В Р РЋРЎвЂєР В Р’В Р РЋРІР‚СћР В Р’В Р В РІР‚В Р В Р’В Р вЂ™Р’В°Р В Р Р‹Р В РІР‚С™Р В Р Р‹Р Р†Р вЂљРІвЂћвЂ“",
                    callback_data="admin:products",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Р РЋР вЂљР РЋРЎСџР Р†Р вЂљР’ВР вЂ™Р’В· Р В Р’В Р РЋРІР‚С”Р В Р’В Р РЋРІР‚вЂќР В Р’В Р вЂ™Р’ВµР В Р Р‹Р В РІР‚С™Р В Р’В Р вЂ™Р’В°Р В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р РЋРІР‚СћР В Р Р‹Р В РІР‚С™Р В Р Р‹Р Р†Р вЂљРІвЂћвЂ“",
                    callback_data="admin:operators",
                ),
                InlineKeyboardButton(
                    text="Р РЋР вЂљР РЋРЎСџР В Р РЏР вЂ™Р’В¦ Р В Р’В Р Р†Р вЂљР’ВР В Р’В Р вЂ™Р’В°Р В Р’В Р В РІР‚В¦Р В Р’В Р РЋРІР‚СњР В Р’В Р РЋРІР‚В",
                    callback_data="admin:banks",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Р РЋР вЂљР РЋРЎСџР Р†Р вЂљРЎС™Р В РІР‚В° Р В Р’В Р В Р вЂ№Р В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р вЂ™Р’В°Р В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р РЋРІР‚ВР В Р Р‹Р В РЎвЂњР В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р РЋРІР‚ВР В Р’В Р РЋРІР‚СњР В Р’В Р вЂ™Р’В°",
                    callback_data="admin:stats",
                ),
            ],
        ]
    )

