# bot/keyboards/admin/entities.py
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.callbacks_admin import AdminWarehouseSelectCB


def entity_list_kb(
    items: list[tuple[int, str]],
    cb_factory,
    warehouse_id: int,
) -> InlineKeyboardMarkup:
    rows = []

    for entity_id, title in items:
        rows.append([
            InlineKeyboardButton(
                text=title,
                callback_data=cb_factory(entity_id=entity_id).pack(),
            )
        ])

    rows.append([
        InlineKeyboardButton(
            text="А ⬅️ В корзину",
            callback_data=AdminWarehouseSelectCB(
                warehouse_id=warehouse_id
            ).pack(),
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=rows)