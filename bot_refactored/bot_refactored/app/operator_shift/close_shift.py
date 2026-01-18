from sqlalchemy.ext.asyncio import AsyncSession
from bot_refactored.dao.operator_shift import OperatorShiftDAO
from bot_refactored.domain.operator_shift import OperatorShiftDomain, ShiftStateError


class CloseShiftUseCase:
    def __init__(self, operator_id: int, session: AsyncSession):
        self.operator_id = operator_id
        self.session = session

    async def execute(self):
        async with self.session.begin():
            shift = await OperatorShiftDAO.get_active_for_update(
                self.session, self.operator_id
            )
            if not shift:
                raise ShiftStateError("no active shift")

            OperatorShiftDomain(shift.state).can_close()
            await OperatorShiftDAO.close(shift)

