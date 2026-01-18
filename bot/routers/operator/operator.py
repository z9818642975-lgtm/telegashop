from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.role import RoleFilter
from bot.models.enums import UserRole
from bot.models.user import User
from bot.dao.operator_shift_dao import OperatorShiftDAO
from bot.keyboards.operator.shift import on_shift_kb, off_shift_kb, confirm_shift_kb
from bot.constants.callbacks import CB
from bot.fsm.operator_shift_fsm import OperatorShiftFSM

router = Router(name="operator_shift")
router.callback_query.filter(RoleFilter(UserRole.OPERATOR))
router.message.filter(RoleFilter(UserRole.OPERATOR))


@router.callback_query(F.data == CB.OP_SHIFT_START)
async def shift_start(
    call: CallbackQuery,
    state: FSMContext,
):
    await state.set_state(OperatorShiftFSM.enter_address)
    await call.message.edit_text(
        "📍 Введите адрес самовывоза:",
    )
    await call.answer()


@router.message(OperatorShiftFSM.enter_address)
async def shift_address(
    message: Message,
    state: FSMContext,
):
    await state.update_data(pickup_address=message.text)
    await state.set_state(OperatorShiftFSM.confirm)

    await message.answer(
        f"📍 Адрес:\n{message.text}\n\nПодтвердить выход на смену?",
        reply_markup=confirm_shift_kb,
    )


@router.callback_query(F.data == CB.OP_SHIFT_CONFIRM, OperatorShiftFSM.confirm)
async def shift_confirm(
    call: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    user: User,
):
    data = await state.get_data()
    shifts = OperatorShiftDAO(session)

    await shifts.start_shift(
        operator_id=user.id,
        pickup_address=data["pickup_address"],
    )
    await session.commit()
    await state.clear()

    await call.message.edit_text(
        f"✅ Смена активна\n\n📍 Адрес:\n{data['pickup_address']}",
        reply_markup=off_shift_kb,
    )
    await call.answer()


@router.callback_query(F.data == CB.OP_SHIFT_STOP)
async def shift_stop(
    call: CallbackQuery,
    session: AsyncSession,
    user: User,
):
    shifts = OperatorShiftDAO(session)

    if not await shifts.is_on_shift(user.id):
        await call.answer("❌ Смена не активна", show_alert=True)
        return

    await shifts.stop_shift(operator_id=user.id)
    await session.commit()

    await call.message.edit_text(
        "❌ Смена завершена",
        reply_markup=on_shift_kb,
    )
    await call.answer()

