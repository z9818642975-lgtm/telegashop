from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.constants.callbacks import CB
from bot.keyboards.client.common import back_btn


def quantity_kb(product_id: int) -> InlineKeyboardMarkup:
    row_1 = [
        InlineKeyboardButton(
            text=str(i),
            callback_data=CB.QTY.format(id=product_id, qty=i),
        )
        for i in range(1, 6)
    ]

    row_2 = [
        InlineKeyboardButton(
            text=str(i),
            callback_data=CB.QTY.format(id=product_id, qty=i),
        )
        for i in range(6, 11)
    ]

    return InlineKeyboardMarkup(
        inline_keyboard=[
            row_1,
            row_2,
            [
                back_btn(
                    "⬅️ К товару",
                    CB.BACK_PRODUCT.format(id=product_id),
                )
            ],
        ]
    )

