from sqlalchemy.ext.asyncio import AsyncSession
from bot_refactored.dao.operator_shift import OperatorShiftDAO
from bot_refactored.domain.operator_shift import OperatorShiftDomain


class OpenShiftUseCase:
    def __init__(self, operator_id: int, pickup_address: str, session: AsyncSession):
        self.operator_id = operator_id
        self.pickup_address = pickup_address
        self.session = session

    async def execute(self):
        async with self.session.begin():
            active = await OperatorShiftDAO.get_active_for_update(
                self.session, self.operator_id
            )
            if active:
                OperatorShiftDomain(active.state).can_open()

            await OperatorShiftDAO.create_open(
                self.session, self.operator_id, self.pickup_address
            )

