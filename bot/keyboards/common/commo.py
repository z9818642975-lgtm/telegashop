# bot/keyboards/common/commo.py
from aiogram.types import InlineKeyboardButton

from bot.constants.callbacks_common import ClientCartOpen

# bot/keyboards/inline/common.py





def back_btn(callback_data: str):


    return InlineKeyboardButton(


        text="⬅ Назад",


        callback_data=ClientCartOpen().pack(),


    )







