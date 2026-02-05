# bot/keyboards/admin/stocks.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.callbacks_admin import AdminWarehouseSelectCB, AdminWarehousesStockCB


def admin_stocks_kb(warehouses) -> InlineKeyboardMarkup:
    rows = []
    row = []

    for wh in warehouses:
        row.append(
            InlineKeyboardButton(
                text=f"🏬 {wh.title}",
                callback_data=AdminWarehousesStockCB(
                    warehouse_id=wh.id
                ).pack(),
            )
        )
        if len(row) == 2:
            rows.append(row)
            row = []

    if row:
        rows.append(row)

    rows.append([
        InlineKeyboardButton(
            text="А ⬅️ В корзину",
            callback_data=AdminWarehouseSelectCB(warehouse_id=wh.id).pack()
,
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=rows)