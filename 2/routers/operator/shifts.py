from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.role import RoleFilter
from bot.dao.operator_shift_dao import OperatorShiftDAO, OperatorShiftStateError
from bot.keyboards.operator.main import operator_main_menu
from bot.fsm.operator_shift_fsm import OperatorShiftFSM

router = Router(name="operator_shift")

# ============================================================
# START SHIFT (STEP 1) — кнопка "🟢 Выйти на смену"
# ============================================================

@router.message(
    RoleFilter("operator"),
    F.text == "🟢 Выйти на смену",
)
async def start_shift_request(
    message: Message,
    state: FSMContext,
):
    await state.set_state(OperatorShiftFSM.pickup_address)
    await message.answer(
        "📍 Введите адрес самовывоза:",
    )

# ============================================================
# START SHIFT (STEP 2) — ввод адреса
# ============================================================

@router.message(
    RoleFilter("operator"),
    OperatorShiftFSM.pickup_address,
)
async def start_shift_confirm(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    user,
):
    address = message.text.strip()
    if not address:
        await message.answer("❌ Адрес не может быть пустым")
        return

    shifts = OperatorShiftDAO(session)

    try:
        await shifts.start_shift(
            operator_id=user.id,
            pickup_address=address,
        )
    except OperatorShiftStateError:
        await message.answer(
            "⚠️ Смена уже активна",
            reply_markup=operator_main_menu(on_shift=True),
        )
        await state.clear()
        return

    await session.commit()
    await state.clear()

    await message.answer(
        f"✅ Смена начата\n\n📍 Самовывоз:\n{address}",
        reply_markup=operator_main_menu(on_shift=True),
    )

# ============================================================
# STOP SHIFT
# ============================================================

@router.message(
    RoleFilter("operator"),
    F.text == "⏸ Закрыть смену",
)
async def stop_shift(
    message: Message,
    session: AsyncSession,
    user,
):
    shifts = OperatorShiftDAO(session)

    if not await shifts.is_on_shift(user.id):
        await message.answer(
            "⚠️ Смена не активна",
            reply_markup=operator_main_menu(on_shift=False),
        )
        return

    await shifts.stop_shift(operator_id=user.id)
    await session.commit()

    await message.answer(
        "🔴 Смена завершена",
        reply_markup=operator_main_menu(on_shift=False),
    )

