# bot/keyboards/admin/warehouses.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.callbacks_admin import AdminWarehouseSelectCB
from bot.constants.callbacks_common import BackCB


def warehouses_kb(items: list) -> InlineKeyboardMarkup:
    rows = []

    for wh in items:
        rows.append([
            InlineKeyboardButton(
                text=f"🏬 {wh.title}",
                callback_data=AdminWarehouseSelectCB(
                    warehouse_id=wh.id
                ).pack(),
            )
        ])

    rows.append([
        InlineKeyboardButton(
            text="А ⬅️ В корзину",
            callback_data=BackCB(target="admin_menu").pack()
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=rows)