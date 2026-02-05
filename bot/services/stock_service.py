# bot/services/stock_service.py
from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from bot.dao.products_dao import ProductsDAO
from bot.dao.reservations_dao import ReservationsDAO
from bot.dao.restock_dao import RestockDAO
from bot.dao.warehouse_products_dao import WarehouseProductsDAO
from bot.dao.warehouses_dao import WarehousesDAO
from bot.services.admin_notify_service import AdminNotifyService


class StockService:
    def __init__(self, s: AsyncSession):
        self.s = s
        self.warehouses = WarehousesDAO(s)
        self.wp = WarehouseProductsDAO(s)
        self.res = ReservationsDAO(s)
        self.products = ProductsDAO(s)          # ✅ FIX
        self.restock = RestockDAO(s)
        self.notify = AdminNotifyService()

    async def _warehouse_for_order(self, order):
        if order.delivery_method == "COURIER":
            wh = await self.warehouses.get_admin()
        else:
            wh = await self.warehouses.get_operator(order.operator_id or 0)

        if not wh:
            raise ValueError("Склад не найден")

        return wh

    async def reserve_for_order(self, order, items, bot=None):
        wh = await self._warehouse_for_order(order)

        for it in items:
            have = await self.wp.get_qty(wh.id, it["product_id"])
            if have < it["qty"]:
                raise ValueError("Недостаточно товара на складе")

            # списание
            await self.wp.add(wh.id, it["product_id"], -it["qty"])  # ✅ вместо decrease

            await self.res.create(
                order_id=order.id,
                warehouse_id=wh.id,
                product_id=it["product_id"],
                qty=it["qty"],
                status="RESERVED",
            )

            await self._low_stock_check(
                wh.id,
                it["product_id"],
                bot,
                wh.title,
            )

        await self.s.commit()

    async def consume(self, order_id: int):
        rs = await self.res.list_by_order(order_id)
        for r in rs:
            r.status = "USED"
        await self.s.commit()

    async def move_reservation(self, order_id: int, new_operator_tg_id: int):
        rs = await self.res.list_by_order(order_id)
        new_wh = await self.warehouses.get_operator(new_operator_tg_id)

        if not new_wh:
            raise ValueError("Нет склада нового оператора")

        for r in rs:
            r.status = "RELEASED"
            await self.res.create(
                order_id=order_id,
                warehouse_id=new_wh.id,
                product_id=r.product_id,
                qty=r.qty,
                status="RESERVED",
            )

        await self.s.commit()

    async def _low_stock_check(self, warehouse_id: int, product_id: int, bot, warehouse_title: str):
        row = await self.wp.get_row(warehouse_id, product_id)
        if not row:
            return

        product = await self.products.get(product_id)
        if not product or product.min_qty is None:
            return

        if row.qty_available <= product.min_qty and not row.low_notified:
            row.low_notified = True

            if not await self.restock.has_active(product_id, warehouse_id):
                await self.restock.create(
                    product_id=product_id,
                    warehouse_id=warehouse_id,
                    qty=max(product.min_qty * 3, 10),
                    status="CREATED",
                )

            if bot:
                await self.notify.low_stock(
                    bot,
                    product.title,
                    row.qty_available,
                    warehouse_title,
                )