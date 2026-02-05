# bot/routers/demo.py
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from bot.constants.callbacks_demo import DemoCB
from bot.keyboards.demo import demo_kb

router = Router(name="demo")

@router.message(F.text == "/demo")
async def demo_start(msg: Message):
    await msg.answer("Demo menu", reply_markup=demo_kb())

@router.callback_query(DemoCB.filter())
async def demo_click(cb: CallbackQuery, callback_data: DemoCB):
    await cb.answer()
    await cb.message.edit_text(
        f"Нажата кнопка: {callback_data.action}",
        reply_markup=demo_kb()
    )
