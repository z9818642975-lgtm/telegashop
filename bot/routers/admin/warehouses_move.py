# bot/routers/admin/warehouses_move.py
from __future__ import annotations

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.constants.callbacks_admin import AdminWarehouseSelectCB
from bot.dao.warehouse_movement_dao import WarehouseMovementDAO
from bot.dao.warehouses_dao import WarehousesDAO
from bot.filters.role import RoleFilter
from bot.fsm.admin_move_fsm import AdminMoveFSM
from bot.utils.safe_edit import safe_edit_text

router = Router(name="admin_warehouse_move")


# ============================================================
# START
# ============================================================

@router.callback_query(RoleFilter("admin"), F.data == "admin_wh_move_start")
async def move_start(
    cb: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
):
    dao = WarehousesDAO(session)
    warehouses = await dao.list_active()

    if len(warehouses) < 2:
        await cb.answer("Недостаточно складов", show_alert=True)
        return

    await state.set_state(AdminMoveFSM.from_warehouse)

    rows = [
        [
            InlineKeyboardButton(
                text=f"🏬 {w.title}",
                callback_data=AdminWarehouseSelectCB(
                    warehouse_id=w.id
                ).pack(),
            )
        ]
        for w in warehouses
    ]

    await safe_edit_text(
        cb.message,
        text="А 🔁 <b>Перемещение товара</b>\n\nВыберите склад-источник:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=rows),
        parse_mode="HTML",
    )
    await cb.answer()


# ============================================================
# FROM / TO — ОДИН CB
# ============================================================

@router.callback_query(RoleFilter("admin"), AdminWarehouseSelectCB.filter())
async def choose_warehouse(
    cb: CallbackQuery,
    callback_data: AdminWarehouseSelectCB,
    state: FSMContext,
    session: AsyncSession,
):
    data = await state.get_data()

    # ---------- выбор FROM ----------
    if "from_wh" not in data:
        await state.update_data(from_wh=callback_data.warehouse_id)
        await state.set_state(AdminMoveFSM.to_warehouse)

        dao = WarehousesDAO(session)
        warehouses = await dao.list_active()

        rows = [
            [
                InlineKeyboardButton(
                    text=f"🏬 {w.title}",
                    callback_data=AdminWarehouseSelectCB(
                        warehouse_id=w.id
                    ).pack(),
                )
            ]
            for w in warehouses
            if w.id != callback_data.warehouse_id
        ]

        await safe_edit_text(
            cb.message,
            text="А ➡️ Выберите склад-получатель:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=rows),
        )
        await cb.answer()
        return

    # ---------- выбор TO ----------
    await state.update_data(to_wh=callback_data.warehouse_id)
    await state.set_state(AdminMoveFSM.product)

    await safe_edit_text(
        cb.message,
        text="А 📦 Введите ID товара:",
    )
    await cb.answer()


# ============================================================
# PRODUCT
# ============================================================

@router.message(RoleFilter("admin"), AdminMoveFSM.product)
async def enter_product(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Введите числовой ID товара")
        return

    await state.update_data(product_id=int(message.text))
    await state.set_state(AdminMoveFSM.qty)

    await message.answer("🔢 Введите количество:")


# ============================================================
# QTY → MOVE
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

    qty = int(message.text)
    if qty <= 0:
        await message.answer("❌ Количество должно быть > 0")
        return

    data = await state.get_data()

    wh_dao = WarehousesDAO(session)
    move_dao = WarehouseMovementDAO(session)

    await wh_dao.move_product(
        product_id=data["product_id"],
        qty=qty,
        from_wh_id=data["from_wh"],
        to_wh_id=data["to_wh"],
    )

    await move_dao.create(
        product_id=data["product_id"],
        qty=qty,
        from_wh_id=data["from_wh"],
        to_wh_id=data["to_wh"],
        reason="ADMIN_MOVE",
        actor_id=message.from_user.id,
    )

    await session.commit()
    await state.clear()

    await message.answer(
        f"✅ Перемещение выполнено\n"
        f"Товар #{data['product_id']}\n"
        f"{qty} шт."
    )

