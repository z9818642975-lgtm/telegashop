# bot/dao/warehouse_products_dao.py
from sqlalchemy import select

# bot/dao/warehouse_products_dao.py
from sqlalchemy import select


from sqlalchemy.ext.asyncio import AsyncSession


from bot.models.warehouse_product import WarehouseProduct








class WarehouseProductsDAO:


    def __init__(self, s: AsyncSession):


        self.s = s





    async def get_row(self, warehouse_id: int, product_id: int) -> WarehouseProduct | None:


        res = await self.s.execute(


            select(WarehouseProduct).where(


                WarehouseProduct.warehouse_id == warehouse_id,


                WarehouseProduct.product_id == product_id,


            )


        )


        return res.scalar_one_or_none()





    async def get_qty(self, warehouse_id: int, product_id: int) -> int:


        row = await self.get_row(warehouse_id, product_id)


        return row.qty_available if row else 0





    async def add(self, warehouse_id: int, product_id: int, qty: int) -> None:


        row = await self.get_row(warehouse_id, product_id)


        if row:


            row.qty_available += qty


            return


        row = WarehouseProduct(warehouse_id=warehouse_id, product_id=product_id, qty_available=qty, low_notified=False)


        self.s.add(row)





    async def move(self, from_wh: int, to_wh: int, product_id: int, qty: int) -> None:


        if qty <= 0:


            raise ValueError("qty must be > 0")


        from_row = await self.get_row(from_wh, product_id)


        if not from_row or from_row.qty_available < qty:


            raise ValueError("not enough stock")


        from_row.qty_available -= qty


        await self.add(to_wh, product_id, qty)





