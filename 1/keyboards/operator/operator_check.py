# bot/keyboards/inline/operator_check.py


# bot/keyboards/inline/operator_check.py



from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton





def operator_check_kb(order_id: int):


    return InlineKeyboardMarkup(


        inline_keyboard=[


            [


                InlineKeyboardButton(text="РІСљвЂ¦ Р СџРЎР‚Р С‘Р Р…РЎРЏРЎвЂљРЎРЉ РЎвЂЎР ВµР С”", callback_data=f"op:check:accept:{order_id}"),


                InlineKeyboardButton(text="РІСњРЉ Р С›РЎвЂљР С”Р В»Р С•Р Р…Р С‘РЎвЂљРЎРЉ РЎвЂЎР ВµР С”", callback_data=f"op:check:reject:{order_id}")


            ]


        ]


    )





