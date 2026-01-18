from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.constants.callbacks import CB


def payment_method_kb() -> InlineKeyboardMarkup:
    """
    Р вЂ™РЎвЂ№Р В±Р С•РЎР‚ РЎРѓР С—Р С•РЎРѓР С•Р В±Р В° Р С•Р С—Р В»Р В°РЎвЂљРЎвЂ№
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="СЂСџРЏВ¦ Р вЂР В°Р Р…Р С”Р С•Р Р†РЎРѓР С”Р В°РЎРЏ Р С”Р В°РЎР‚РЎвЂљР В°",
                    callback_data=CB.PAY_BANK.format(bank_id="any"),
                )
            ],
            [
                InlineKeyboardButton(
                    text="СЂСџвЂњВ± Р РЋР вЂР Сџ",
                    callback_data=CB.PAY_SBP,
                )
            ],
            [
                InlineKeyboardButton(
                    text="РІВ¬вЂ¦РїС‘РЏ Р СњР В°Р В·Р В°Р Т‘",
                    callback_data=CB.CART_OPEN,
                )
            ],
        ]
    )


def payment_confirm_kb() -> InlineKeyboardMarkup:
    """
    Р СџР С•Р Т‘РЎвЂљР Р†Р ВµРЎР‚Р В¶Р Т‘Р ВµР Р…Р С‘Р Вµ Р С•Р С—Р В»Р В°РЎвЂљРЎвЂ№
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="РІСљвЂ¦ Р Р‡ Р С•Р С—Р В»Р В°РЎвЂљР С‘Р В»",
                    callback_data=CB.PAYMENT_DONE,
                )
            ],
            [
                InlineKeyboardButton(
                    text="РІСњРЉ Р С›РЎвЂљР СР ВµР Р…Р В°",
                    callback_data=CB.PAYMENT_CANCEL,
                )
            ],
        ]
    )


# РЎРЊР С”РЎРѓР С—Р С•РЎР‚РЎвЂљ Р Т‘Р В»РЎРЏ client/__init__.py
def payment_kb() -> InlineKeyboardMarkup:
    return payment_method_kb()

