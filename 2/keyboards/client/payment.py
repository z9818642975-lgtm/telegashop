from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.constants.callbacks import CB


def payment_method_kb() -> InlineKeyboardMarkup:
    """
    Выбор способа оплаты
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🏦 Банковская карта",
                    callback_data=CB.PAY_BANK.format(bank_id="any"),
                )
            ],
            [
                InlineKeyboardButton(
                    text="📱 СБП",
                    callback_data=CB.PAY_SBP,
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data=CB.CART_OPEN,
                )
            ],
        ]
    )


def payment_confirm_kb() -> InlineKeyboardMarkup:
    """
    Подтверждение оплаты
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Я оплатил",
                    callback_data=CB.PAYMENT_DONE,
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Отмена",
                    callback_data=CB.PAYMENT_CANCEL,
                )
            ],
        ]
    )


# экспорт для client/__init__.py
def payment_kb() -> InlineKeyboardMarkup:
    return payment_method_kb()

