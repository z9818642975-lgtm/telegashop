# bot/routers/operator/shifts.py
from aiogram import F, Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.dao.operator_shift_dao import OperatorShiftDAO
from bot.keyboards.operator.main import operator_main_menu_kb

router = Router(name="operator_shifts")


@router.message(F.text == "🟢 Начать смену")
async def start_shift(
    message: Message,
    session: AsyncSession,
    user,
):
    dao = OperatorShiftDAO(session)

    active = await dao.get_active(user.id)
    if active:
        await message.answer(
            "⚠️ Смена уже активна",
            reply_markup=operator_main_menu_kb(on_shift=True),
        )
        return

    await dao.start(
        operator_id=user.id,
        pickup_address="—",  # по контракту вводится при старте
    )
    await session.commit()

    await message.answer(
        "✅ Смена начата",
        reply_markup=operator_main_menu_kb(on_shift=True),
    )


@router.message(F.text == "🔴 Завершить смену")
async def stop_shift(
    message: Message,
    session: AsyncSession,
    user,
):
    dao = OperatorShiftDAO(session)

    active = await dao.get_active(user.id)
    if not active:
        await message.answer(
            "⚠️ Смена не активна",
            reply_markup=operator_main_menu_kb(on_shift=False),
        )
        return

    await dao.stop(operator_id=user.id)
    await session.commit()

    await message.answer(
        "🔴 Смена завершена",
        reply_markup=operator_main_menu_kb(on_shift=False),
    )
