# bot/keyboards/inline/operator_check.py


# bot/keyboards/inline/operator_check.py



from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton





def operator_check_kb(order_id: int):


    return InlineKeyboardMarkup(


        inline_keyboard=[


            [


                InlineKeyboardButton(text="✅ Принять чек", callback_data=f"op:check:accept:{order_id}"),


                InlineKeyboardButton(text="❌ Отклонить чек", callback_data=f"op:check:reject:{order_id}")


            ]


        ]


    )





