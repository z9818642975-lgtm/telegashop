from sqlalchemy.ext.asyncio import AsyncSession
from bot_refactored.dao.central_inventory import CentralInventoryDAO
from bot_refactored.dao.inventory import InventoryDAO

class TransferToOperatorUseCase:
    def __init__(
        self,
        *,
        product_id: int,
        qty: int,
        operator_id: int,
        session: AsyncSession,
    ):
        self.product_id = product_id
        self.qty = qty
        self.operator_id = operator_id
        self.session = session

    async def execute(self):
        async with self.session.begin():
            central = await CentralInventoryDAO.get_for_update(
                self.session, self.product_id
            )
            if not central or central.quantity < self.qty:
                raise ValueError("not enough central stock")

            central.quantity -= self.qty

            item = await InventoryDAO.get_for_update(
                self.session,
                operator_id=self.operator_id,
                product_id=self.product_id,
            )
            if not item:
                raise ValueError("operator inventory not found")

            item.quantity += self.qty

