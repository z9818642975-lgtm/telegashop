# bot/keyboards/operator/operator_order.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.constants.callbacks import CB


def operator_order_kb(order_id: int) -> InlineKeyboardMarkup:
    """
    Основная клавиатура оператора для заказа
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Принять",
                    callback_data=CB.OP_CHECK_ACCEPT.format(id=order_id),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🏁 Завершить",
                    callback_data=CB.OP_READY.format(id=order_id),
                ),
                InlineKeyboardButton(
                    text="🔙 Назад",
                    callback_data="operator:orders",
                ),
            ],
        ]
    )


def ready_kb(order_id: int) -> InlineKeyboardMarkup:
    """
    Кнопка «Заказ готов»
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📦 Заказ готов",
                    callback_data=CB.OP_READY.format(id=order_id),
                )
            ]
        ]
    )


def sent_kb(order_id: int) -> InlineKeyboardMarkup:
    """
    Кнопка «Заказ передан / выдан»
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚚 Передан клиенту",
                    callback_data=CB.OP_SENT.format(id=order_id),
                )
            ]
        ]
    )

