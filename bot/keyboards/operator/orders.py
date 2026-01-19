from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.constants.callbacks import CB


def operator_order_kb(order_id: int) -> InlineKeyboardMarkup:
    """
    Базовая карточка заказа (до готовности)
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Принять чек",
                    callback_data=CB.OP_CHECK_ACCEPT.format(id=order_id),
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Назад",
                    callback_data="operator:orders",
                )
            ],
        ]
    )


def ready_pickup_kb(order_id: int) -> InlineKeyboardMarkup:
    """
    Самовывоз → 📦 Заказ готов
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📦 Заказ готов",
                    callback_data=f"operator:ready:{order_id}",
                )
            ]
        ]
    )


def sent_kb(order_id: int) -> InlineKeyboardMarkup:
    """
    Универсальная кнопка:
    - самовывоз → «Передан клиенту»
    - доставка → «Передан курьеру»
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚚 Передан",
                    callback_data=f"operator:sent:{order_id}",
                )
            ]
        ]
    )

