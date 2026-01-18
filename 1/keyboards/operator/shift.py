from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.constants.callbacks import CB

on_shift_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("СЂСџС™Р‚ Р вЂ™РЎвЂ№Р в„–РЎвЂљР С‘ Р Р…Р В° РЎРѓР СР ВµР Р…РЎС“", callback_data=CB.OP_SHIFT_START)]
    ]
)

off_shift_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("РІвЂєвЂќ Р вЂ”Р В°Р Р†Р ВµРЎР‚РЎв‚¬Р С‘РЎвЂљРЎРЉ РЎРѓР СР ВµР Р…РЎС“", callback_data=CB.OP_SHIFT_STOP)],
        [InlineKeyboardButton("РІСљРЏРїС‘РЏ Р ВР В·Р СР ВµР Р…Р С‘РЎвЂљРЎРЉ Р В°Р Т‘РЎР‚Р ВµРЎРѓ", callback_data=CB.OP_SHIFT_EDIT_ADDRESS)],
    ]
)

confirm_shift_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("РІСљвЂ¦ Р СџР С•Р Т‘РЎвЂљР Р†Р ВµРЎР‚Р Т‘Р С‘РЎвЂљРЎРЉ", callback_data=CB.OP_SHIFT_CONFIRM)],
        [InlineKeyboardButton("РІСњРЉ Р С›РЎвЂљР СР ВµР Р…Р В°", callback_data=CB.OP_SHIFT_CANCEL)],
    ]
)

