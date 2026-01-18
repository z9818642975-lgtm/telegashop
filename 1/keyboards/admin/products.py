from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.models.product import Product


def products_kb(products: list[Product]) -> InlineKeyboardMarkup:
    keyboard = []

    for p in products:
        status = "Р РЋР вЂљР РЋРЎСџР РЋРЎСџР РЋРЎвЂє" if p.is_active else "Р В Р вЂ Р РЋРІвЂћСћР вЂ™Р’В«Р В РЎвЂ”Р РЋРІР‚ВР В Р РЏ"
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{status} {p.title} ({p.base_price} Р В Р вЂ Р Р†Р вЂљРЎв„ўР В РІР‚В¦)",
                    callback_data=f"admin:product:card:{p.id}",
                )
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="Р В Р вЂ Р РЋРІР‚С”Р Р†Р вЂљРЎС› Р В Р’В Р Р†Р вЂљРЎСљР В Р’В Р РЋРІР‚СћР В Р’В Р вЂ™Р’В±Р В Р’В Р вЂ™Р’В°Р В Р’В Р В РІР‚В Р В Р’В Р РЋРІР‚ВР В Р Р‹Р Р†Р вЂљРЎв„ўР В Р Р‹Р В Р вЂ° Р В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р РЋРІР‚СћР В Р’В Р В РІР‚В Р В Р’В Р вЂ™Р’В°Р В Р Р‹Р В РІР‚С™",
                callback_data="admin:product:create",
            )
        ]
    )
    keyboard.append(
        [
            InlineKeyboardButton(
                text="Р В Р вЂ Р вЂ™Р’В¬Р Р†Р вЂљР’В¦Р В РЎвЂ”Р РЋРІР‚ВР В Р РЏ Р В Р’В Р РЋРЎС™Р В Р’В Р вЂ™Р’В°Р В Р’В Р вЂ™Р’В·Р В Р’В Р вЂ™Р’В°Р В Р’В Р СћРІР‚В",
                callback_data="admin:panel",
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

