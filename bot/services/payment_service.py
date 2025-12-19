from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from bot.dao.orders_dao import OrdersDAO
from bot.dao.payments_dao import PaymentsDAO
from bot.services.bank_balancer_service import BankBalancerService
from bot.services.bank_stats_service import BankStatsService
from bot.models.enums import OrderStatus

class PaymentService:
    def __init__(self, s: AsyncSession):
        self.s = s
        self.orders = OrdersDAO(s)
        self.payments = PaymentsDAO(s)
        self.balancer = BankBalancerService(s)
        self.stats = BankStatsService(s)

    async def pick_account_for_order(self, order_id: int, bank_id: int):
        account = await self.balancer.pick_account(bank_id)
        await self.orders.attach_payment_choice(order_id, bank_id=bank_id, bank_account_id=account.id)
        await self.stats.shown(bank_id, account.id, order_id)
        await self.s.commit()

        if account.sbp_phone:
            return {"type":"SBP", "bank": account.bank_name, "sbp": account.sbp_phone, "card": None, "account_id": account.id}
        return {"type":"CARD", "bank": account.bank_name, "sbp": None, "card": account.card_masked or account.card_number, "account_id": account.id}

    async def attach_proof(self, order_id: int, file_id: str):
        await self.payments.create_or_update_proof(order_id, file_id)
        await self.s.commit()

    async def confirm_payment(self, order_id: int, operator_tg_id: int):
        pay = await self.payments.get(order_id)
        if not pay or not pay.proof_file_id:
            raise ValueError("Нет чека")
        await self.payments.confirm(order_id, operator_tg_id)
        await self.orders.set_status(order_id, OrderStatus.PAID.value)
        order = await self.orders.get(order_id)
        await self.stats.paid(order.bank_id or 0, order.bank_account_id, order_id)
        await self.s.commit()
