from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.callbacks_admin import (
    AdminWarehouseDeactivateCB,
    AdminWarehouseMoveCB,
    AdminWarehouseProductsCB,
    AdminWarehousesListCB,
)


def admin_warehouse_actions_kb(warehouse_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📦 Товары на складе",
                callback_data=AdminWarehouseProductsCB(
                    warehouse_id=warehouse_id
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="🔁 Переместить товары",
                callback_data=AdminWarehouseMoveCB(
                    warehouse_id=warehouse_id
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="🛑 Архивировать склад",
                callback_data=AdminWarehouseDeactivateCB(
                    warehouse_id=warehouse_id
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ К складам",
                callback_data=AdminWarehousesListCB().pack(),
            )
        ],
    ])
warehouse_actions_kb = admin_warehouse_actions_kb
