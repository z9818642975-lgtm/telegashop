# bot/routers/admin/warehouses_move.py

# bot/routers/admin/warehouses_move.py
# bot/routers/admin/warehouses_move.py


from __future__ import annotations





from aiogram import Router, F


from aiogram.types import CallbackQuery, Message


from aiogram.fsm.context import FSMContext


from sqlalchemy.ext.asyncio import AsyncSession





from bot.filters.role import RoleFilter


from bot.fsm.admin_move_fsm import AdminMoveFSM


from bot.dao.warehouses_dao import WarehousesDAO


from bot.dao.products_dao import ProductsDAO





router = Router(name="admin_warehouse_move")








# ============================================================


# Р РЋР вЂљР РЋРЎСџР Р†Р вЂљРЎСљР В РЎвЂњ Р В Р’В Р Р†Р вЂљРІвЂћСћР В Р’В Р вЂ™Р’В«Р В Р’В Р Р†Р вЂљР’ВР В Р’В Р РЋРІР‚С”Р В Р’В Р вЂ™Р’В  Р В Р’В Р вЂ™Р’ВР В Р’В Р В Р вЂ№Р В Р’В Р СћРЎвЂ™Р В Р’В Р РЋРІР‚С”Р В Р’В Р Р†Р вЂљРЎСљР В Р’В Р РЋРЎС™Р В Р’В Р РЋРІР‚С”Р В Р’В Р Р†Р вЂљРЎС™Р В Р’В Р РЋРІР‚С” Р В Р’В Р В Р вЂ№Р В Р’В Р РЋРІвЂћСћР В Р’В Р Р†Р вЂљРЎвЂќР В Р’В Р РЋРІР‚в„ўР В Р’В Р Р†Р вЂљРЎСљР В Р’В Р РЋРІР‚в„ў


# ============================================================





@router.callback_query(RoleFilter("admin"), F.data == "admin:move:start")


async def move_start(call: CallbackQuery, state: FSMContext | None = None, session: AsyncSession | None = None):


    dao = WarehousesDAO(session)


    warehouses = await dao.get_all()





    await state.set_state(AdminMoveFSM.from_warehouse)





    text = "Р РЋР вЂљР РЋРЎСџР Р†Р вЂљРЎСљР В РЎвЂњ <b>Р В Р’В Р РЋРЎСџР В Р’В Р вЂ™Р’ВµР В Р Р‹Р В РІР‚С™Р В Р’В Р вЂ™Р’ВµР В Р’В Р РЋР’ВР В Р’В Р вЂ™Р’ВµР В Р Р‹Р Р†Р вЂљР’В°Р В Р’В Р вЂ™Р’ВµР В Р’В Р В РІР‚В¦Р В Р’В Р РЋРІР‚ВР В Р’В Р вЂ™Р’Вµ Р В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р РЋРІР‚СћР В Р’В Р В РІР‚В Р В Р’В Р вЂ™Р’В°Р В Р Р‹Р В РІР‚С™Р В Р’В Р вЂ™Р’В°</b>\n\nР В Р’В Р Р†Р вЂљРІвЂћСћР В Р Р‹Р Р†Р вЂљРІвЂћвЂ“Р В Р’В Р вЂ™Р’В±Р В Р’В Р вЂ™Р’ВµР В Р Р‹Р В РІР‚С™Р В Р’В Р РЋРІР‚ВР В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р вЂ™Р’Вµ Р В Р Р‹Р В РЎвЂњР В Р’В Р РЋРІР‚СњР В Р’В Р вЂ™Р’В»Р В Р’В Р вЂ™Р’В°Р В Р’В Р СћРІР‚В-Р В Р’В Р РЋРІР‚ВР В Р Р‹Р В РЎвЂњР В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р РЋРІР‚СћР В Р Р‹Р Р†Р вЂљР Р‹Р В Р’В Р В РІР‚В¦Р В Р’В Р РЋРІР‚ВР В Р’В Р РЋРІР‚Сњ:"


    kb = [


        [("Р РЋР вЂљР РЋРЎСџР В Р РЏР вЂ™Р’В¬ " + w.title, f"admin:move:from:{w.id}")]


        for w in warehouses


    ]





    await call.message.edit_text(text, reply_markup=dao.inline_kb(kb))








# ============================================================


# Р РЋР вЂљР РЋРЎСџР В Р РЏР вЂ™Р’В¬ FROM


# ============================================================





@router.callback_query(RoleFilter("admin"), F.data.startswith("admin:move:from:"))


async def choose_from(


    call: CallbackQuery,


    state: FSMContext | None = None,


):


    from_id = int(call.data.split(":")[-1])


    await state.update_data(from_wh=from_id)


    await state.set_state(AdminMoveFSM.to_warehouse)





    await call.message.edit_text("Р В Р вЂ Р РЋРІР‚С”Р В Р вЂ№Р В РЎвЂ”Р РЋРІР‚ВР В Р РЏ Р В Р’В Р Р†Р вЂљРІвЂћСћР В Р Р‹Р Р†Р вЂљРІвЂћвЂ“Р В Р’В Р вЂ™Р’В±Р В Р’В Р вЂ™Р’ВµР В Р Р‹Р В РІР‚С™Р В Р’В Р РЋРІР‚ВР В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р вЂ™Р’Вµ Р В Р Р‹Р В РЎвЂњР В Р’В Р РЋРІР‚СњР В Р’В Р вЂ™Р’В»Р В Р’В Р вЂ™Р’В°Р В Р’В Р СћРІР‚В-Р В Р’В Р РЋРІР‚вЂќР В Р’В Р РЋРІР‚СћР В Р’В Р вЂ™Р’В»Р В Р Р‹Р РЋРІР‚СљР В Р Р‹Р Р†Р вЂљР Р‹Р В Р’В Р вЂ™Р’В°Р В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р вЂ™Р’ВµР В Р’В Р вЂ™Р’В»Р В Р Р‹Р В Р вЂ°:")








# ============================================================


# Р РЋР вЂљР РЋРЎСџР В Р РЏР вЂ™Р’В¬ TO


# ============================================================





@router.callback_query(RoleFilter("admin"), F.data.startswith("admin:move:to:"))


async def choose_to(


    call: CallbackQuery,


    state: FSMContext | None = None,


):


    to_id = int(call.data.split(":")[-1])


    await state.update_data(to_wh=to_id)


    await state.set_state(AdminMoveFSM.product)





    await call.message.edit_text("Р РЋР вЂљР РЋРЎСџР Р†Р вЂљРЎС™Р вЂ™Р’В¦ Р В Р’В Р Р†Р вЂљРІвЂћСћР В Р’В Р В РІР‚В Р В Р’В Р вЂ™Р’ВµР В Р’В Р СћРІР‚ВР В Р’В Р РЋРІР‚ВР В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р вЂ™Р’Вµ ID Р В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р РЋРІР‚СћР В Р’В Р В РІР‚В Р В Р’В Р вЂ™Р’В°Р В Р Р‹Р В РІР‚С™Р В Р’В Р вЂ™Р’В°:")








# ============================================================


# Р РЋР вЂљР РЋРЎСџР Р†Р вЂљРЎС™Р вЂ™Р’В¦ PRODUCT


# ============================================================





@router.message(RoleFilter("admin"), AdminMoveFSM.product)


async def enter_product(message, *, state: FSMContext | None = None,


):


    if not message.text.isdigit():


        await message.answer("Р В Р вЂ Р РЋРЎС™Р В Р вЂ° Р В Р’В Р Р†Р вЂљРІвЂћСћР В Р’В Р В РІР‚В Р В Р’В Р вЂ™Р’ВµР В Р’В Р СћРІР‚ВР В Р’В Р РЋРІР‚ВР В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р вЂ™Р’Вµ Р В Р Р‹Р Р†Р вЂљР Р‹Р В Р’В Р РЋРІР‚ВР В Р Р‹Р В РЎвЂњР В Р’В Р вЂ™Р’В»Р В Р’В Р РЋРІР‚СћР В Р’В Р В РІР‚В Р В Р’В Р РЋРІР‚СћР В Р’В Р Р†РІР‚С›РІР‚вЂњ ID Р В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р РЋРІР‚СћР В Р’В Р В РІР‚В Р В Р’В Р вЂ™Р’В°Р В Р Р‹Р В РІР‚С™Р В Р’В Р вЂ™Р’В°")


        return





    await state.update_data(product_id=int(message.text))


    await state.set_state(AdminMoveFSM.qty)





    await message.answer("Р РЋР вЂљР РЋРЎСџР Р†Р вЂљРЎСљР РЋРЎвЂє Р В Р’В Р Р†Р вЂљРІвЂћСћР В Р’В Р В РІР‚В Р В Р’В Р вЂ™Р’ВµР В Р’В Р СћРІР‚ВР В Р’В Р РЋРІР‚ВР В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р вЂ™Р’Вµ Р В Р’В Р РЋРІР‚СњР В Р’В Р РЋРІР‚СћР В Р’В Р вЂ™Р’В»Р В Р’В Р РЋРІР‚ВР В Р Р‹Р Р†Р вЂљР Р‹Р В Р’В Р вЂ™Р’ВµР В Р Р‹Р В РЎвЂњР В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р В РІР‚В Р В Р’В Р РЋРІР‚Сћ:")








# ============================================================


# Р РЋР вЂљР РЋРЎСџР Р†Р вЂљРЎСљР РЋРЎвЂє QTY Р В Р вЂ Р Р†Р вЂљР’В Р Р†Р вЂљРІвЂћСћ MOVE


# ============================================================





@router.message(RoleFilter("admin"), AdminMoveFSM.qty)


async def do_move(message, *, state: FSMContext | None = None,


    session: AsyncSession | None = None,


):


    if not message.text.isdigit():


        await message.answer("Р В Р вЂ Р РЋРЎС™Р В Р вЂ° Р В Р’В Р РЋРІвЂћСћР В Р’В Р РЋРІР‚СћР В Р’В Р вЂ™Р’В»Р В Р’В Р РЋРІР‚ВР В Р Р‹Р Р†Р вЂљР Р‹Р В Р’В Р вЂ™Р’ВµР В Р Р‹Р В РЎвЂњР В Р Р‹Р Р†Р вЂљРЎв„ўР В Р’В Р В РІР‚В Р В Р’В Р РЋРІР‚Сћ Р В Р’В Р СћРІР‚ВР В Р’В Р РЋРІР‚СћР В Р’В Р вЂ™Р’В»Р В Р’В Р вЂ™Р’В¶Р В Р’В Р В РІР‚В¦Р В Р’В Р РЋРІР‚Сћ Р В Р’В Р вЂ™Р’В±Р В Р Р‹Р Р†Р вЂљРІвЂћвЂ“Р В Р Р‹Р Р†Р вЂљРЎв„ўР В Р Р‹Р В Р вЂ° Р В Р Р‹Р Р†Р вЂљР Р‹Р В Р’В Р РЋРІР‚ВР В Р Р‹Р В РЎвЂњР В Р’В Р вЂ™Р’В»Р В Р’В Р РЋРІР‚СћР В Р’В Р РЋР’В")


        return





    data = await state.get_data()





    qty = int(message.text)


    from_wh = data["from_wh"]


    to_wh = data["to_wh"]


    product_id = data["product_id"]





    wh_dao = WarehousesDAO(session)


    products = await ProductsDAO.list_all(session)





    await wh_dao.move_product(


        product_id=product_id,


        qty=qty,


        from_wh_id=from_wh,


        to_wh_id=to_wh,


    )





    await session.commit()


    await state.clear()





    await message.answer(


        f"Р В Р вЂ Р РЋРЎв„ўР Р†Р вЂљР’В¦ Р В Р’В Р РЋРЎСџР В Р’В Р вЂ™Р’ВµР В Р Р‹Р В РІР‚С™Р В Р’В Р вЂ™Р’ВµР В Р’В Р РЋР’ВР В Р’В Р вЂ™Р’ВµР В Р Р‹Р Р†Р вЂљР’В°Р В Р’В Р вЂ™Р’ВµР В Р’В Р В РІР‚В¦Р В Р’В Р РЋРІР‚ВР В Р’В Р вЂ™Р’Вµ Р В Р’В Р В РІР‚В Р В Р Р‹Р Р†Р вЂљРІвЂћвЂ“Р В Р’В Р РЋРІР‚вЂќР В Р’В Р РЋРІР‚СћР В Р’В Р вЂ™Р’В»Р В Р’В Р В РІР‚В¦Р В Р’В Р вЂ™Р’ВµР В Р’В Р В РІР‚В¦Р В Р’В Р РЋРІР‚Сћ\n"


        f"Р В Р’В Р РЋРЎвЂєР В Р’В Р РЋРІР‚СћР В Р’В Р В РІР‚В Р В Р’В Р вЂ™Р’В°Р В Р Р‹Р В РІР‚С™ #{product_id}\n"


        f"{qty} Р В Р Р‹Р Р†РІР‚С™Р’В¬Р В Р Р‹Р Р†Р вЂљРЎв„ў."


    )






