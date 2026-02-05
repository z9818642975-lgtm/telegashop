# bot/dao/warehouses_dao.py
from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.warehouse import Warehouse
from bot.models.warehouse_movement import WarehouseMovement
from bot.models.warehouse_product import WarehouseProduct


class StockError(Exception):
    pass


# ============================================================
# WAREHOUSES DAO
# ============================================================

class WarehousesDAO:
    """
    DAO ТОЛЬКО ДЛЯ СКЛАДОВ И ОСТАТКОВ
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    # -------------------- WAREHOUSES --------------------

    async def list_active(self) -> List[Warehouse]:
        res = await self.session.execute(
            select(Warehouse)
            .where(Warehouse.is_active.is_(True))
            .order_by(Warehouse.id)
        )
        return res.scalars().all()

    async def get_by_id(self, warehouse_id: int) -> Warehouse | None:
        return await self.session.get(Warehouse, warehouse_id)

    async def get_admin(self) -> Warehouse | None:
        res = await self.session.execute(
            select(Warehouse)
            .where(
                Warehouse.is_admin.is_(True),
                Warehouse.is_active.is_(True),
            )
            .limit(1)
        )
        return res.scalar_one_or_none()

    async def get_operator(self, operator_id: int) -> Warehouse | None:
        res = await self.session.execute(
            select(Warehouse)
            .where(
                Warehouse.operator_id == operator_id,
                Warehouse.is_active.is_(True),
            )
            .limit(1)
        )
        return res.scalar_one_or_none()

    # -------------------- STOCK --------------------

    async def get_stock(
        self,
        *,
        warehouse_id: int,
        product_id: int,
    ) -> WarehouseProduct | None:
        res = await self.session.execute(
            select(WarehouseProduct).where(
                WarehouseProduct.warehouse_id == warehouse_id,
                WarehouseProduct.product_id == product_id,
            )
        )
        return res.scalar_one_or_none()

    async def decrease_stock(
        self,
        *,
        warehouse_id: int,
        product_id: int,
        qty: int,
    ) -> None:
        res = await self.session.execute(
            select(WarehouseProduct)
            .where(
                WarehouseProduct.warehouse_id == warehouse_id,
                WarehouseProduct.product_id == product_id,
            )
            .with_for_update()
        )
        row = res.scalar_one_or_none()

        if not row:
            raise StockError("Товар отсутствует на складе")

        if row.qty_available < qty:
            raise StockError(
                f"Недостаточно товара: доступно {row.qty_available}, требуется {qty}"
            )

        row.qty_available -= qty

    async def increase_stock(
        self,
        *,
        warehouse_id: int,
        product_id: int,
        qty: int,
    ) -> None:
        res = await self.session.execute(
            select(WarehouseProduct)
            .where(
                WarehouseProduct.warehouse_id == warehouse_id,
                WarehouseProduct.product_id == product_id,
            )
            .with_for_update()
        )
        row = res.scalar_one_or_none()

        if not row:
            row = WarehouseProduct(
                warehouse_id=warehouse_id,
                product_id=product_id,
                qty_available=0,
            )
            self.session.add(row)

        row.qty_available += qty

    async def move_product(
        self,
        *,
        product_id: int,
        qty: int,
        from_wh_id: int,
        to_wh_id: int,
    ) -> None:
        await self.decrease_stock(
            warehouse_id=from_wh_id,
            product_id=product_id,
            qty=qty,
        )
        await self.increase_stock(
            warehouse_id=to_wh_id,
            product_id=product_id,
            qty=qty,
        )


# ============================================================
# WAREHOUSE MOVEMENT DAO (AUDIT)
# ============================================================

class WarehouseMovementDAO:
    """
    Аудит движения товара.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        *,
        product_id: int,
        qty: int,
        from_wh_id: int | None,
        to_wh_id: int | None,
        reason: str,
        actor_id: int | None = None,
    ) -> WarehouseMovement:
        movement = WarehouseMovement(
            product_id=product_id,
            qty=qty,
            from_warehouse_id=from_wh_id,
            to_warehouse_id=to_wh_id,
            reason=reason,
            actor_id=actor_id,
            created_at=datetime.utcnow(),
        )
        self.session.add(movement)
        await self.session.flush()
        return movement
