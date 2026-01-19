from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def quantity_kb(order_item_id: int) -> InlineKeyboardMarkup:
    """
    Клавиатура выбора количества товара.
    Количество УСТАНАВЛИВАЕТСЯ (замена), не суммируется.
    ❌ Без кнопки «Назад»
    """

    # 1–5
    row1 = [
        InlineKeyboardButton(
            text=str(i),
            callback_data=f"client:item:qty:{order_item_id}:{i}"
        )
        for i in range(1, 6)
    ]

    # 6–10
    row2 = [
        InlineKeyboardButton(
            text=str(i),
            callback_data=f"client:item:qty:{order_item_id}:{i}"
        )
        for i in range(6, 11)
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=[row1, row2]
    )
