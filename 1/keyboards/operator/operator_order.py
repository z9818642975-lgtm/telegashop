# bot/keyboards/operator/operator_order.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.constants.callbacks import CB


def operator_order_kb(order_id: int) -> InlineKeyboardMarkup:
    """
    Р В РЎвЂєР РЋР С“Р В Р вЂ¦Р В РЎвЂўР В Р вЂ Р В Р вЂ¦Р В Р’В°Р РЋР РЏ Р В РЎвЂќР В Р’В»Р В Р’В°Р В Р вЂ Р В РЎвЂР В Р’В°Р РЋРІР‚С™Р РЋРЎвЂњР РЋР вЂљР В Р’В° Р В РЎвЂўР В РЎвЂ”Р В Р’ВµР РЋР вЂљР В Р’В°Р РЋРІР‚С™Р В РЎвЂўР РЋР вЂљР В Р’В° Р В РўвЂР В Р’В»Р РЋР РЏ Р В Р’В·Р В Р’В°Р В РЎвЂќР В Р’В°Р В Р’В·Р В Р’В°
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Р Р†РЎС™РІР‚В¦ Р В РЎСџР РЋР вЂљР В РЎвЂР В Р вЂ¦Р РЋР РЏР РЋРІР‚С™Р РЋР Р‰",
                    callback_data=CB.OP_CHECK_ACCEPT.format(id=order_id),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="РЎР‚РЎСџР РЏР С“ Р В РІР‚вЂќР В Р’В°Р В Р вЂ Р В Р’ВµР РЋР вЂљР РЋРІвЂљВ¬Р В РЎвЂР РЋРІР‚С™Р РЋР Р‰",
                    callback_data=CB.OP_READY.format(id=order_id),
                ),
                InlineKeyboardButton(
                    text="РЎР‚РЎСџРІР‚СњРІвЂћСћ Р В РЎСљР В Р’В°Р В Р’В·Р В Р’В°Р В РўвЂ",
                    callback_data="operator:op:orders",
                ),
            ],
        ]
    )


def ready_kb(order_id: int) -> InlineKeyboardMarkup:
    """
    Р В РЎв„ўР В Р вЂ¦Р В РЎвЂўР В РЎвЂ”Р В РЎвЂќР В Р’В° Р вЂ™Р’В«Р В РІР‚вЂќР В Р’В°Р В РЎвЂќР В Р’В°Р В Р’В· Р В РЎвЂ“Р В РЎвЂўР РЋРІР‚С™Р В РЎвЂўР В Р вЂ Р вЂ™Р’В»
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="РЎР‚РЎСџРІР‚СљР’В¦ Р В РІР‚вЂќР В Р’В°Р В РЎвЂќР В Р’В°Р В Р’В· Р В РЎвЂ“Р В РЎвЂўР РЋРІР‚С™Р В РЎвЂўР В Р вЂ ",
                    callback_data=CB.OP_READY.format(id=order_id),
                )
            ]
        ]
    )


def sent_kb(order_id: int) -> InlineKeyboardMarkup:
    """
    Р В РЎв„ўР В Р вЂ¦Р В РЎвЂўР В РЎвЂ”Р В РЎвЂќР В Р’В° Р вЂ™Р’В«Р В РІР‚вЂќР В Р’В°Р В РЎвЂќР В Р’В°Р В Р’В· Р В РЎвЂ”Р В Р’ВµР РЋР вЂљР В Р’ВµР В РўвЂР В Р’В°Р В Р вЂ¦ / Р В Р вЂ Р РЋРІР‚в„–Р В РўвЂР В Р’В°Р В Р вЂ¦Р вЂ™Р’В»
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="РЎР‚РЎСџРЎв„ўРЎв„ў Р В РЎСџР В Р’ВµР РЋР вЂљР В Р’ВµР В РўвЂР В Р’В°Р В Р вЂ¦ Р В РЎвЂќР В Р’В»Р В РЎвЂР В Р’ВµР В Р вЂ¦Р РЋРІР‚С™Р РЋРЎвЂњ",
                    callback_data=CB.OP_SENT.format(id=order_id),
                )
            ]
        ]
    )

