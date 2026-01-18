from sqlalchemy.ext.asyncio import AsyncSession
from bot_refactored.dao.operators import OperatorsDAO

class CreateOperatorUseCase:
    def __init__(self, telegram_id: int, session: AsyncSession):
        self.telegram_id = telegram_id
        self.session = session

    async def execute(self):
        async with self.session.begin():
            await OperatorsDAO.create(self.session, self.telegram_id)

class ArchiveOperatorUseCase:
    def __init__(self, telegram_id: int, session: AsyncSession):
        self.telegram_id = telegram_id
        self.session = session

    async def execute(self):
        async with self.session.begin():
            await OperatorsDAO.archive(self.session, self.telegram_id)

