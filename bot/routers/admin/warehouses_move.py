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


# 🔁 ВЫБОР ИСХОДНОГО СКЛАДА


# ============================================================





@router.callback_query(RoleFilter("admin"), F.data == "admin:move:start")


async def move_start(call: CallbackQuery, state: FSMContext, session: AsyncSession):


    dao = WarehousesDAO(session)


    warehouses = await dao.get_all()





    await state.set_state(AdminMoveFSM.from_warehouse)





    text = "🔁 <b>Перемещение товара</b>\n\nВыберите склад-источник:"


    kb = [


        [("🏬 " + w.title, f"admin:move:from:{w.id}")]


        for w in warehouses


    ]





    await call.message.edit_text(text, reply_markup=dao.inline_kb(kb))








# ============================================================


# 🏬 FROM


# ============================================================





@router.callback_query(RoleFilter("admin"), F.data.startswith("admin:move:from:"))


async def choose_from(


    call: CallbackQuery,


    state: FSMContext,


):


    from_id = int(call.data.split(":")[-1])


    await state.update_data(from_wh=from_id)


    await state.set_state(AdminMoveFSM.to_warehouse)





    await call.message.edit_text("➡️ Выберите склад-получатель:")








# ============================================================


# 🏬 TO


# ============================================================





@router.callback_query(RoleFilter("admin"), F.data.startswith("admin:move:to:"))


async def choose_to(


    call: CallbackQuery,


    state: FSMContext,


):


    to_id = int(call.data.split(":")[-1])


    await state.update_data(to_wh=to_id)


    await state.set_state(AdminMoveFSM.product)





    await call.message.edit_text("📦 Введите ID товара:")








# ============================================================


# 📦 PRODUCT


# ============================================================





@router.message(RoleFilter("admin"), AdminMoveFSM.product)


async def enter_product(


    message: Message,


    state: FSMContext,


):


    if not message.text.isdigit():


        await message.answer("❌ Введите числовой ID товара")


        return





    await state.update_data(product_id=int(message.text))


    await state.set_state(AdminMoveFSM.qty)





    await message.answer("🔢 Введите количество:")








# ============================================================


# 🔢 QTY → MOVE


# ============================================================





@router.message(RoleFilter("admin"), AdminMoveFSM.qty)


async def do_move(


    message: Message,


    state: FSMContext,


    session: AsyncSession,


):


    if not message.text.isdigit():


        await message.answer("❌ Количество должно быть числом")


        return





    data = await state.get_data()





    qty = int(message.text)


    from_wh = data["from_wh"]


    to_wh = data["to_wh"]


    product_id = data["product_id"]





    wh_dao = WarehousesDAO(session)


    products = await ProductsDAO(session).list_all()





    await wh_dao.move_product(


        product_id=product_id,


        qty=qty,


        from_wh_id=from_wh,


        to_wh_id=to_wh,


    )





    await session.commit()


    await state.clear()





    await message.answer(


        f"✅ Перемещение выполнено\n"


        f"Товар #{product_id}\n"


        f"{qty} шт."


    )




