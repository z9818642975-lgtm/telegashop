# bot/routers/debug.py
#C:\Users\1\project\bot\routers\debug.py

# bot/routers/debug.py
#C:\Users\1\project\bot\routers\debug.py


from aiogram import Router


from aiogram.types import CallbackQuery, Message





router = Router(name="debug")





@router.callback_query()


async def debug_cb(call: CallbackQuery):


    print("CB:", call.data)





@router.message()


async def debug_msg(message: Message):


    print("MSG:", message.text)





