from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def warehouse_actions_kb(warehouse_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📦 Товары на складе",
                    callback_data=f"admin:wh:{warehouse_id}:products",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔁 Переместить товары",
                    callback_data=f"admin:wh:{warehouse_id}:move",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="❌ Деактивировать склад",
                    callback_data=f"admin:wh:{warehouse_id}:disable",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="admin:warehouses",
                ),
            ],
        ]
    )

