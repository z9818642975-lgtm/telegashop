# bot/keyboards/admin/force_actions.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def force_actions_kb(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="РІвЂєвЂќ Р СџРЎР‚Р С‘Р Р…РЎС“Р Т‘Р С‘РЎвЂљР ВµР В»РЎРЉР Р…Р С• Р В·Р В°Р С”РЎР‚РЎвЂ№РЎвЂљРЎРЉ",
                    callback_data=f"admin:force:close:{order_id}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="СЂСџвЂќвЂћ Р вЂ™Р ВµРЎР‚Р Р…РЎС“РЎвЂљРЎРЉ Р Р† РЎР‚Р В°Р В±Р С•РЎвЂљРЎС“",
                    callback_data=f"admin:force:reopen:{order_id}",
                ),
            ],
        ]
    )

