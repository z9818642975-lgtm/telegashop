from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.callbacks import CB
from bot.dao.operators import OperatorsDAO
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router(name="admin_operators_crud")

@router.callback_query(F.data == CB.ADMIN_OPERATORS)
async def list_ops(cb: CallbackQuery, *, session: AsyncSession | None = None):
    ops = await OperatorsDAO.list(session)
    kb = []
    for op in ops:
        kb.append([
            InlineKeyboardButton(
                text=f"рџ‘· {op.tg_id}",
                callback_data=f"{CB.ADMIN_OPERATOR_ARCHIVE}{op.id}",
            )
        ])
    kb.append(
        [InlineKeyboardButton("вћ• Р”РѕР±Р°РІРёС‚СЊ РѕРїРµСЂР°С‚РѕСЂР°", callback_data=CB.ADMIN_OPERATOR_ADD)]
    )

    await cb.message.edit_text(
        "рџ‘· <b>РћРїРµСЂР°С‚РѕСЂС‹</b>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=kb),
    )
    await cb.answer()

@router.callback_query(F.data.startswith(CB.ADMIN_OPERATOR_ARCHIVE))
async def archive_op(cb: CallbackQuery, *, session: AsyncSession | None = None):
    op_id = int(cb.data.split(":")[-1])
    await OperatorsDAO.archive(session, op_id)
    await cb.answer("РћРїРµСЂР°С‚РѕСЂ Р°СЂС…РёРІРёСЂРѕРІР°РЅ")


