from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.operator_salary import OperatorSalary

class SalaryService:
    @staticmethod
    async def accrue(session: AsyncSession, operator_id: int, order_id: int, amount: int):
        salary = OperatorSalary(
            operator_id=operator_id,
            order_id=order_id,
            amount=amount,
        )
        session.add(salary)

