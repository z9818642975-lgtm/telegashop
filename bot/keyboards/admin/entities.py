from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def entity_list(entity: str, items: list[tuple[int, str]]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=name,
                    callback_data=f"{entity}:card:{entity_id}",
                )
            ]
            for entity_id, name in items
        ]
    )


def entity_card(entity: str, entity_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✏️ Изменить",
                    callback_data=f"{entity}:edit:{entity_id}",
                ),
                InlineKeyboardButton(
                    text="🗑 Удалить",
                    callback_data=f"{entity}:delete:{entity_id}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data=f"{entity}:list",
                ),
            ],
        ]
    )

