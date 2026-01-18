from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def operator_pickup_ready_kb(order_id: int) -> InlineKeyboardMarkup:
    """
    Р РЋР В°Р СР С•Р Р†РЎвЂ№Р Р†Р С•Р В· РІвЂ вЂ™ Р’В«СЂСџвЂњВ¦ Р вЂ”Р В°Р С”Р В°Р В· Р С–Р С•РЎвЂљР С•Р Р†Р’В»
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="СЂСџвЂњВ¦ Р вЂ”Р В°Р С”Р В°Р В· Р С–Р С•РЎвЂљР С•Р Р†",
                    callback_data=f"op:pickup:ready:{order_id}",
                )
            ]
        ]
    )


def operator_delivery_sent_kb(order_id: int) -> InlineKeyboardMarkup:
    """
    Р вЂќР С•РЎРѓРЎвЂљР В°Р Р†Р С”Р В° РІвЂ вЂ™ Р’В«СЂСџС™С™ Р СџР ВµРЎР‚Р ВµР Т‘Р В°Р Р… Р С”РЎС“РЎР‚РЎРЉР ВµРЎР‚РЎС“Р’В»
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="СЂСџС™С™ Р СџР ВµРЎР‚Р ВµР Т‘Р В°Р Р… Р С”РЎС“РЎР‚РЎРЉР ВµРЎР‚РЎС“",
                    callback_data=f"op:delivery:sent:{order_id}",
                )
            ]
        ]
    )

