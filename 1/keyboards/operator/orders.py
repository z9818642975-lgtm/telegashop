from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.constants.callbacks import CB


def operator_order_kb(order_id: int) -> InlineKeyboardMarkup:
    """
    Р В РІР‚ВР В Р’В°Р В Р’В·Р В РЎвЂўР В Р вЂ Р В Р’В°Р РЋР РЏ Р В РЎвЂќР В Р’В°Р РЋР вЂљР РЋРІР‚С™Р В РЎвЂўР РЋРІР‚РЋР В РЎвЂќР В Р’В° Р В Р’В·Р В Р’В°Р В РЎвЂќР В Р’В°Р В Р’В·Р В Р’В° (Р В РўвЂР В РЎвЂў Р В РЎвЂ“Р В РЎвЂўР РЋРІР‚С™Р В РЎвЂўР В Р вЂ Р В Р вЂ¦Р В РЎвЂўР РЋР С“Р РЋРІР‚С™Р В РЎвЂ)
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Р Р†РЎС™РІР‚В¦ Р В РЎСџР РЋР вЂљР В РЎвЂР В Р вЂ¦Р РЋР РЏР РЋРІР‚С™Р РЋР Р‰ Р РЋРІР‚РЋР В Р’ВµР В РЎвЂќ",
                    callback_data=CB.OP_CHECK_ACCEPT.format(id=order_id),
                )
            ],
            [
                InlineKeyboardButton(
                    text="РЎР‚РЎСџРІР‚СњРІвЂћСћ Р В РЎСљР В Р’В°Р В Р’В·Р В Р’В°Р В РўвЂ",
                    callback_data="operator:op:orders",
                )
            ],
        ]
    )


def ready_pickup_kb(order_id: int) -> InlineKeyboardMarkup:
    """
    Р В Р Р‹Р В Р’В°Р В РЎВР В РЎвЂўР В Р вЂ Р РЋРІР‚в„–Р В Р вЂ Р В РЎвЂўР В Р’В· Р Р†РІР‚В РІР‚в„ў РЎР‚РЎСџРІР‚СљР’В¦ Р В РІР‚вЂќР В Р’В°Р В РЎвЂќР В Р’В°Р В Р’В· Р В РЎвЂ“Р В РЎвЂўР РЋРІР‚С™Р В РЎвЂўР В Р вЂ 
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="РЎР‚РЎСџРІР‚СљР’В¦ Р В РІР‚вЂќР В Р’В°Р В РЎвЂќР В Р’В°Р В Р’В· Р В РЎвЂ“Р В РЎвЂўР РЋРІР‚С™Р В РЎвЂўР В Р вЂ ",
                    callback_data=f"op:ready:{order_id}",
                )
            ]
        ]
    )


def sent_kb(order_id: int) -> InlineKeyboardMarkup:
    """
    Р В Р в‚¬Р В Р вЂ¦Р В РЎвЂР В Р вЂ Р В Р’ВµР РЋР вЂљР РЋР С“Р В Р’В°Р В Р’В»Р РЋР Р‰Р В Р вЂ¦Р В Р’В°Р РЋР РЏ Р В РЎвЂќР В Р вЂ¦Р В РЎвЂўР В РЎвЂ”Р В РЎвЂќР В Р’В°:
    - Р РЋР С“Р В Р’В°Р В РЎВР В РЎвЂўР В Р вЂ Р РЋРІР‚в„–Р В Р вЂ Р В РЎвЂўР В Р’В· Р Р†РІР‚В РІР‚в„ў Р вЂ™Р’В«Р В РЎСџР В Р’ВµР РЋР вЂљР В Р’ВµР В РўвЂР В Р’В°Р В Р вЂ¦ Р В РЎвЂќР В Р’В»Р В РЎвЂР В Р’ВµР В Р вЂ¦Р РЋРІР‚С™Р РЋРЎвЂњР вЂ™Р’В»
    - Р В РўвЂР В РЎвЂўР РЋР С“Р РЋРІР‚С™Р В Р’В°Р В Р вЂ Р В РЎвЂќР В Р’В° Р Р†РІР‚В РІР‚в„ў Р вЂ™Р’В«Р В РЎСџР В Р’ВµР РЋР вЂљР В Р’ВµР В РўвЂР В Р’В°Р В Р вЂ¦ Р В РЎвЂќР РЋРЎвЂњР РЋР вЂљР РЋР Р‰Р В Р’ВµР РЋР вЂљР РЋРЎвЂњР вЂ™Р’В»
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="РЎР‚РЎСџРЎв„ўРЎв„ў Р В РЎСџР В Р’ВµР РЋР вЂљР В Р’ВµР В РўвЂР В Р’В°Р В Р вЂ¦",
                    callback_data=f"op:sent:{order_id}",
                )
            ]
        ]
    )

