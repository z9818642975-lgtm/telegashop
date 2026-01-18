from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def operator_pickup_ready_kb(order_id: int) -> InlineKeyboardMarkup:
    """
    Самовывоз → «📦 Заказ готов»
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📦 Заказ готов",
                    callback_data=f"op:pickup:ready:{order_id}",
                )
            ]
        ]
    )


def operator_delivery_sent_kb(order_id: int) -> InlineKeyboardMarkup:
    """
    Доставка → «🚚 Передан курьеру»
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚚 Передан курьеру",
                    callback_data=f"op:delivery:sent:{order_id}",
                )
            ]
        ]
    )

