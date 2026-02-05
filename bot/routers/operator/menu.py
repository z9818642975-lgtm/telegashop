# bot/routers/operator/menu.py
from aiogram import F, Router
from aiogram.types import Message

from bot.keyboards.operator.main import operator_main_menu_kb
from bot.keyboards.operator.orders import operator_orders_kb
from bot.keyboards.operator.statistics import operator_stats_kb

router = Router(name="operator_menu")

# ======================
# ENTRY
# ======================

@router.message(F.text == "О ⬅️ В корзину")
async def operator_back_to_menu(message: Message):
    await message.answer(
        "👷 Меню оператора",
        reply_markup=operator_main_menu_kb(on_shift=False),
    )

# ======================
# ORDERS
# ======================

@router.message(F.text == "О 📦 Заказы")
async def operator_orders(message: Message):
    await message.answer(
        "📦 Заказы оператора",
        reply_markup=operator_orders_kb(),
    )

# ======================
# STATS
# ======================

@router.message(F.text == "О 📊 Статистика и ЗП")
async def operator_stats(message: Message):
    await message.answer(
        "📊 Статистика и зарплата",
        reply_markup=operator_stats_kb(),
    )
