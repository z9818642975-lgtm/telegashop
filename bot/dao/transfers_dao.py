# bot/dao/transfers_dao.py
from sqlalchemy.ext.asyncio import AsyncSession

# bot/dao/transfers_dao.py
from sqlalchemy.ext.asyncio import AsyncSession


from bot.models.warehouse_transfer import WarehouseTransfer








class TransfersDAO:


    def __init__(self, session: AsyncSession):
        self.session = session






    async def log(self, from_wh: int, to_wh: int, product_id: int, qty: int, admin_tg_id: int):


        rec = WarehouseTransfer(


            from_warehouse_id=from_wh,


            to_warehouse_id=to_wh,


            product_id=product_id,


            quantity=qty,


            created_by=admin_tg_id,


        )


        self.s.add(rec)


        await self.s.flush()


        return rec





