# bot/dao/statistics.py
from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.enums import OrderStatus, PaymentStatus
from bot.models.operator_shift import OperatorShift
from bot.models.order import Order
from bot.models.payment import Payment
from bot.models.salary_accrual import SalaryAccrual
from bot.models.user import User
from bot.models.warehouse import Warehouse


class StatisticsDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    # =========================================================
    # HELPERS
    # =========================================================

    @staticmethod
    def _today_start() -> datetime:
        return datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    @staticmethod
    def _range(days: int) -> datetime:
        return datetime.utcnow() - timedelta(days=days)

    # =========================================================
    # TODAY SUMMARY
    # =========================================================

    async def today_summary(self) -> dict:
        today = self._today_start()

        orders_total = await self.session.scalar(
            select(func.count(Order.id)).where(Order.created_at >= today)
        )

        orders_paid = await self.session.scalar(
            select(func.count(Order.id)).where(
                Order.created_at >= today,
                Order.status.in_(
                    (OrderStatus.PAID, OrderStatus.READY, OrderStatus.DONE)
                ),
            )
        )

        revenue = await self.session.scalar(
            select(func.coalesce(func.sum(Order.total_price), 0)).where(
                Order.created_at >= today,
                Order.status.in_(
                    (OrderStatus.PAID, OrderStatus.READY, OrderStatus.DONE)
                ),
            )
        )

        operators_total = await self.session.scalar(
            select(func.count(User.id)).where(User.role == "OPERATOR")
        )

        active_shifts = await self.session.scalar(
            select(func.count(OperatorShift.id)).where(
                OperatorShift.ended_at.is_(None)
            )
        )

        salary_today = await self.session.scalar(
            select(func.coalesce(func.sum(SalaryAccrual.amount), 0)).where(
                SalaryAccrual.created_at >= today
            )
        )

        avg_check = int(revenue / orders_paid) if orders_paid else 0

        return {
            "orders_total": orders_total,
            "orders_paid": orders_paid,
            "revenue": revenue,
            "avg_check": avg_check,
            "operators_total": operators_total,
            "active_shifts": active_shifts,
            "salary_today": salary_today,
        }

    # =========================================================
    # ORDERS BY STATUS (TODAY)
    # =========================================================

    async def orders_by_status_today(self) -> dict:
        today = self._today_start()

        rows = await self.session.execute(
            select(Order.status, func.count(Order.id))
            .where(Order.created_at >= today)
            .group_by(Order.status)
        )

        return {status.value: count for status, count in rows.all()}

    # =========================================================
    # ORDER TIMINGS (SLA)
    # =========================================================

    async def order_timings_today(self) -> dict:
        today = self._today_start()

        avg_to_ready = await self.session.scalar(
            select(
                func.avg(
                    func.extract("epoch", Order.ready_at - Order.created_at)
                )
            ).where(
                Order.created_at >= today,
                Order.ready_at.isnot(None),
            )
        )

        return {
            "avg_assembly_min": int(avg_to_ready // 60) if avg_to_ready else 0,
        }

    # =========================================================
    # OPERATOR SLA
    # =========================================================

    async def operators_sla_today(self) -> dict:
        today = self._today_start()

        shifts_total = await self.session.scalar(
            select(func.count(OperatorShift.id)).where(
                OperatorShift.started_at >= today
            )
        )

        shifts_closed = await self.session.scalar(
            select(func.count(OperatorShift.id)).where(
                OperatorShift.started_at >= today,
                OperatorShift.ended_at.isnot(None),
            )
        )

        kicked = await self.session.scalar(
            select(func.count(OperatorShift.id)).where(
                OperatorShift.started_at >= today,
                OperatorShift.kicked.is_(True),
            )
        )

        return {
            "shifts_total": shifts_total,
            "shifts_closed": shifts_closed,
            "kicked": kicked,
        }

    # =========================================================
    # REVENUE BY PAYMENT METHOD
    # =========================================================

    async def revenue_by_method_today(self) -> dict:
        today = self._today_start()

        rows = await self.session.execute(
            select(Payment.method, func.coalesce(func.sum(Payment.amount), 0))
            .where(
                Payment.created_at >= today,
                Payment.status == PaymentStatus.APPROVED,
            )
            .group_by(Payment.method)
        )

        return {method.value: amount for method, amount in rows.all()}

    # =========================================================
    # PERIOD SUMMARY
    # =========================================================

    async def period_summary(self, days: int) -> dict:
        start = self._range(days)

        orders_paid = await self.session.scalar(
            select(func.count(Order.id)).where(
                Order.created_at >= start,
                Order.status.in_(
                    (OrderStatus.PAID, OrderStatus.READY, OrderStatus.DONE)
                ),
            )
        )

        revenue = await self.session.scalar(
            select(func.coalesce(func.sum(Order.total_price), 0)).where(
                Order.created_at >= start,
                Order.status.in_(
                    (OrderStatus.PAID, OrderStatus.READY, OrderStatus.DONE)
                ),
            )
        )

        avg_check = int(revenue / orders_paid) if orders_paid else 0

        return {
            "orders_paid": orders_paid,
            "revenue": revenue,
            "avg_check": avg_check,
        }

    # =========================================================
    # PER OPERATOR
    # =========================================================

    async def per_operator(self, days: int) -> list[dict]:
        start = self._range(days)

        rows = await self.session.execute(
            select(
                User.id,
                User.tg_id.label("operator_tg_id")
,
                func.count(Order.id),
                func.coalesce(func.sum(Order.total_price), 0),
            )
            .join(Order, Order.operator_id == User.id)
            .where(
                Order.created_at >= start,
                Order.status.in_(
                    (OrderStatus.PAID, OrderStatus.READY, OrderStatus.DONE)
                ),
            )
            .group_by(User.id)
            .order_by(func.sum(Order.total_price).desc())
        )

        return [
            {
                "operator_id": uid,
                "name": name or f"#{uid}",
                "orders": orders,
                "revenue": revenue,
            }
            for uid, name, orders, revenue in rows.all()
        ]

    # =========================================================
    # PER WAREHOUSE
    # =========================================================

    async def per_warehouse(self, days: int) -> list[dict]:
        start = self._range(days)

        rows = await self.session.execute(
            select(
                Warehouse.id,
                Warehouse.title,
                func.count(Order.id),
                func.coalesce(func.sum(Order.total_price), 0),
            )
            .join(Order, Order.warehouse_id == Warehouse.id)
            .where(
                Order.created_at >= start,
                Order.status.in_(
                    (OrderStatus.PAID, OrderStatus.READY, OrderStatus.DONE)
                ),
            )
            .group_by(Warehouse.id)
            .order_by(func.sum(Order.total_price).desc())
        )

        return [
            {
                "warehouse_id": wid,
                "title": title,
                "orders": orders,
                "revenue": revenue,
            }
            for wid, title, orders, revenue in rows.all()
        ]

    # =========================================================
    # TIME SERIES
    # =========================================================

    async def revenue_timeseries(self, days: int) -> list[dict]:
        start = self._range(days)

        rows = await self.session.execute(
            select(
                func.date_trunc("day", Order.created_at),
                func.coalesce(func.sum(Order.total_price), 0),
            )
            .where(
                Order.created_at >= start,
                Order.status.in_(
                    (OrderStatus.PAID, OrderStatus.READY, OrderStatus.DONE)
                ),
            )
            .group_by(func.date_trunc("day", Order.created_at))
            .order_by(func.date_trunc("day", Order.created_at))
        )

        return [
            {"date": day.date().isoformat(), "revenue": amount}
            for day, amount in rows.all()
        ]



