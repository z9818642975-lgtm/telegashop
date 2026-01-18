# bot/keyboards/inline/common.py
from aiogram.types import InlineKeyboardButton

# bot/keyboards/inline/common.py
from aiogram.types import InlineKeyboardButton





def back_btn(callback_data: str):


    return InlineKeyboardButton(


        text="⬅ Назад",


        callback_data=callback_data,


    )





