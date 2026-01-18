from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.models.warehouse import Warehouse


def warehouses_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➕ Создать склад",
                    callback_data="admin:warehouse:create",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="admin:panel",
                ),
            ],
        ]
    )


def warehouses_kb(items: list[Warehouse]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"🏬 {wh.title}",
                    callback_data=f"admin:wh:{wh.id}",
                )
            ]
            for wh in items
        ]
    )

