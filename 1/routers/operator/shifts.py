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
# START SHIFT (STEP 1) Р Р†Р вЂљРІР‚Сњ Р В РЎвЂќР В Р вЂ¦Р В РЎвЂўР В РЎвЂ”Р В РЎвЂќР В Р’В° "РЎР‚РЎСџРЎСџРЎС› Р В РІР‚в„ўР РЋРІР‚в„–Р В РІвЂћвЂ“Р РЋРІР‚С™Р В РЎвЂ Р В Р вЂ¦Р В Р’В° Р РЋР С“Р В РЎВР В Р’ВµР В Р вЂ¦Р РЋРЎвЂњ"
# ============================================================

# ❌ DISABLED (admin/operator text handler)
async def start_shift_request(message, *, state: FSMContext | None = None,
):
    await state.set_state(OperatorShiftFSM.pickup_address)
    await message.answer(
        "РЎР‚РЎСџРІР‚СљР РЉ Р В РІР‚в„ўР В Р вЂ Р В Р’ВµР В РўвЂР В РЎвЂР РЋРІР‚С™Р В Р’Вµ Р В Р’В°Р В РўвЂР РЋР вЂљР В Р’ВµР РЋР С“ Р РЋР С“Р В Р’В°Р В РЎВР В РЎвЂўР В Р вЂ Р РЋРІР‚в„–Р В Р вЂ Р В РЎвЂўР В Р’В·Р В Р’В°:",
    )

# ============================================================
# START SHIFT (STEP 2) Р Р†Р вЂљРІР‚Сњ Р В Р вЂ Р В Р вЂ Р В РЎвЂўР В РўвЂ Р В Р’В°Р В РўвЂР РЋР вЂљР В Р’ВµР РЋР С“Р В Р’В°
# ============================================================

@router.message(
    RoleFilter("operator"),
    OperatorShiftFSM.pickup_address,
)
async def start_shift_confirm(message, *, state: FSMContext | None = None,
    session: AsyncSession | None = None,
    user,
):
    address = message.text.strip()
    if not address:
        await message.answer("Р Р†РЎСљР Р‰ Р В РЎвЂ™Р В РўвЂР РЋР вЂљР В Р’ВµР РЋР С“ Р В Р вЂ¦Р В Р’Вµ Р В РЎВР В РЎвЂўР В Р’В¶Р В Р’ВµР РЋРІР‚С™ Р В Р’В±Р РЋРІР‚в„–Р РЋРІР‚С™Р РЋР Р‰ Р В РЎвЂ”Р РЋРЎвЂњР РЋР С“Р РЋРІР‚С™Р РЋРІР‚в„–Р В РЎВ")
        return

    shifts = OperatorShiftDAO(session)

    try:
        await shifts.start_shift(
            operator_id=user.id,
            pickup_address=address,
        )
    except OperatorShiftStateError:
        await message.answer(
            "Р Р†РЎв„ўР’В Р С—РЎвЂР РЏ Р В Р Р‹Р В РЎВР В Р’ВµР В Р вЂ¦Р В Р’В° Р РЋРЎвЂњР В Р’В¶Р В Р’Вµ Р В Р’В°Р В РЎвЂќР РЋРІР‚С™Р В РЎвЂР В Р вЂ Р В Р вЂ¦Р В Р’В°",
            reply_markup=operator_main_menu(on_shift=True),
        )
        await state.clear()
        return

    await session.commit()
    await state.clear()

    await message.answer(
        f"Р Р†РЎС™РІР‚В¦ Р В Р Р‹Р В РЎВР В Р’ВµР В Р вЂ¦Р В Р’В° Р В Р вЂ¦Р В Р’В°Р РЋРІР‚РЋР В Р’В°Р РЋРІР‚С™Р В Р’В°\n\nРЎР‚РЎСџРІР‚СљР РЉ Р В Р Р‹Р В Р’В°Р В РЎВР В РЎвЂўР В Р вЂ Р РЋРІР‚в„–Р В Р вЂ Р В РЎвЂўР В Р’В·:\n{address}",
        reply_markup=operator_main_menu(on_shift=True),
    )

# ============================================================
# STOP SHIFT
# ============================================================

# ❌ DISABLED (admin/operator text handler)
async def stop_shift(message, *, session: AsyncSession | None = None,
    user,
):
    shifts = OperatorShiftDAO(session)

    if not await shifts.is_on_shift(user.id):
        await message.answer(
            "Р Р†РЎв„ўР’В Р С—РЎвЂР РЏ Р В Р Р‹Р В РЎВР В Р’ВµР В Р вЂ¦Р В Р’В° Р В Р вЂ¦Р В Р’Вµ Р В Р’В°Р В РЎвЂќР РЋРІР‚С™Р В РЎвЂР В Р вЂ Р В Р вЂ¦Р В Р’В°",
            reply_markup=operator_main_menu(on_shift=False),
        )
        return

    await shifts.stop_shift(operator_id=user.id)
    await session.commit()

    await message.answer(
        "РЎР‚РЎСџРІР‚СњРўвЂ Р В Р Р‹Р В РЎВР В Р’ВµР В Р вЂ¦Р В Р’В° Р В Р’В·Р В Р’В°Р В Р вЂ Р В Р’ВµР РЋР вЂљР РЋРІвЂљВ¬Р В Р’ВµР В Р вЂ¦Р В Р’В°",
        reply_markup=operator_main_menu(on_shift=False),
    )



