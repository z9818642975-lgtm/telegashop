from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.models.warehouse import Warehouse


def warehouses_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Р В Р вЂ Р РЋРІР‚С”Р Р†Р вЂљРЎС› Р В Р’В Р В Р вЂ№Р В Р’В Р РЋРІР‚СћР В Р’В Р вЂ™Р’В·Р В Р’В Р СћРІР‚ВР В Р’В Р вЂ™Р’В°Р В Р Р‹Р Р†Р вЂљРЎв„ўР В Р Р‹Р В Р вЂ° Р В Р Р‹Р В РЎвЂњР В Р’В Р РЋРІР‚СњР В Р’В Р вЂ™Р’В»Р В Р’В Р вЂ™Р’В°Р В Р’В Р СћРІР‚В",
                    callback_data="admin:warehouse:create",
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


def warehouses_kb(items: list[Warehouse]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"Р РЋР вЂљР РЋРЎСџР В Р РЏР вЂ™Р’В¬ {wh.title}",
                    callback_data=f"admin:wh:{wh.id}",
                )
            ]
            for wh in items
        ]
    )

