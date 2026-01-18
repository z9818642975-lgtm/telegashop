# bot/dao/order_items.py
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.order_item import OrderItem
from bot.models.enums import OrderItemStatus
from bot.exceptions import NotFoundError, InvalidStateError


class OrderItemDAO:
    """
    DAO Р Т‘Р В»РЎРЏ OrderItem РІР‚вЂќ Р С™Р вЂєР В®Р В§Р вЂўР вЂ™Р С’Р Р‡ Р В±Р С‘Р В·Р Р…Р ВµРЎРѓ-Р ВµР Т‘Р С‘Р Р…Р С‘РЎвЂ Р В° Р С—РЎР‚Р С•Р ВµР С”РЎвЂљР В°.

    Р С’РЎР‚РЎвЂ¦Р С‘РЎвЂљР ВµР С”РЎвЂљРЎС“РЎР‚Р Р…РЎвЂ№Р Вµ Р С—РЎР‚Р С‘Р Р…РЎвЂ Р С‘Р С—РЎвЂ№ (Р вЂ”Р С’Р В¤Р ВР С™Р РЋР ВР В Р С›Р вЂ™Р С’Р СњР С›):
    ------------------------------------------------
    1) OrderItem РІР‚вЂќ Р В°РЎвЂљР С•Р СР В°РЎР‚Р Р…Р В°РЎРЏ Р ВµР Т‘Р С‘Р Р…Р С‘РЎвЂ Р В° РЎР‚Р В°Р В±Р С•РЎвЂљРЎвЂ№ Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚Р В°
    2) OrderItem.operator_id РІР‚вЂќ Р Р†Р В»Р В°Р Т‘Р ВµР В»Р ВµРЎвЂ  Р С—Р С•Р В·Р С‘РЎвЂ Р С‘Р С‘
    3) OrderItem.status РІР‚вЂќ Р С‘РЎРѓРЎвЂљР С•РЎвЂЎР Р…Р С‘Р С” Р С‘РЎРѓРЎвЂљР С‘Р Р…РЎвЂ№ Р С—Р С• Р В¶Р С‘Р В·Р Р…Р ВµР Р…Р Р…Р С•Р СРЎС“ РЎвЂ Р С‘Р С”Р В»РЎС“
    4) DONE = РЎвЂљР С•Р Р†Р В°РЎР‚ РЎРѓР С—Р С‘РЎРѓР В°Р Р… Р В»Р С•Р С–Р С‘РЎвЂЎР ВµРЎРѓР С”Р С‘
    5) Warehouse / Р С•РЎРѓРЎвЂљР В°РЎвЂљР С”Р С‘ / Р Т‘Р Р†Р С‘Р В¶Р ВµР Р…Р С‘РЎРЏ РІР‚вЂќ Р СњР вЂў РЎвЂЎР В°РЎРѓРЎвЂљРЎРЉ РЎРЊРЎвЂљР С•Р в„– Р В»Р С•Р С–Р С‘Р С”Р С‘
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    # =========================================================
    # CLIENT FLOW
    # Р вЂќР С•Р В±Р В°Р Р†Р В»Р ВµР Р…Р С‘Р Вµ / РЎС“Р Р†Р ВµР В»Р С‘РЎвЂЎР ВµР Р…Р С‘Р Вµ Р С—Р С•Р В·Р С‘РЎвЂ Р С‘Р С‘ Р Р† Р С”Р С•РЎР‚Р В·Р С‘Р Р…Р Вµ
    # =========================================================

    async def add_or_increment(
        self,
        *,
        order_id: int,
        product_id: int,
        qty: int,
        price: int,
    ) -> OrderItem:
        """
        Р вЂќР С•Р В±Р В°Р Р†Р В»РЎРЏР ВµРЎвЂљ РЎвЂљР С•Р Р†Р В°РЎР‚ Р Р† Р В·Р В°Р С”Р В°Р В· Р С‘Р В»Р С‘ РЎС“Р Р†Р ВµР В»Р С‘РЎвЂЎР С‘Р Р†Р В°Р ВµРЎвЂљ Р С”Р С•Р В»Р С‘РЎвЂЎР ВµРЎРѓРЎвЂљР Р†Р С•,
        Р ВµРЎРѓР В»Р С‘ Р С—Р С•Р В·Р С‘РЎвЂ Р С‘РЎРЏ РЎС“Р В¶Р Вµ Р ВµРЎРѓРЎвЂљРЎРЉ Р Р† Р С”Р С•РЎР‚Р В·Р С‘Р Р…Р Вµ.

        Р ВРЎРѓР С—Р С•Р В»РЎРЉР В·РЎС“Р ВµРЎвЂљРЎРѓРЎРЏ Р СћР С›Р вЂєР В¬Р С™Р С› Р Р…Р В° Р С”Р В»Р С‘Р ВµР Р…РЎвЂљРЎРѓР С”Р С•Р С РЎРЊРЎвЂљР В°Р С—Р Вµ (Р Т‘Р С• Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚Р В°).
        """

        stmt = select(OrderItem).where(
            OrderItem.order_id == order_id,
            OrderItem.product_id == product_id,
        )
        res = await self.session.execute(stmt)
        item = res.scalar_one_or_none()

        if item:
            item.qty += qty
        else:
            item = OrderItem(
                order_id=order_id,
                product_id=product_id,
                qty=qty,
                price=price,
                status=OrderItemStatus.NEW,
            )
            self.session.add(item)

        await self.session.flush()
        return item

    # =========================================================
    # BASE
    # =========================================================

    async def get_by_id(
        self,
        *,
        item_id: int,
        for_update: bool = False,
    ) -> OrderItem:
        """
        Р СџР С•Р В»РЎС“РЎвЂЎР ВµР Р…Р С‘Р Вµ OrderItem Р С—Р С• ID.

        for_update=True Р С‘РЎРѓР С—Р С•Р В»РЎРЉР В·РЎС“Р ВµРЎвЂљРЎРѓРЎРЏ:
        - Р Р† Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚РЎРѓР С”Р С‘РЎвЂ¦ РЎРѓРЎвЂ Р ВµР Р…Р В°РЎР‚Р С‘РЎРЏРЎвЂ¦
        - Р Т‘Р В»РЎРЏ Р В·Р В°РЎвЂ°Р С‘РЎвЂљРЎвЂ№ Р С•РЎвЂљ Р С–Р С•Р Р…Р С•Р С” РЎРѓРЎвЂљР В°РЎвЂљРЎС“РЎРѓР С•Р Р†
        """
        return await self.session.get(
            OrderItem,
            item_id,
            with_for_update=for_update,
        )

    # =========================================================
    # OPERATOR FLOW
    # Р вЂ“Р С‘Р В·Р Р…Р ВµР Р…Р Р…РЎвЂ№Р в„– РЎвЂ Р С‘Р С”Р В» Р С—Р С•Р В·Р С‘РЎвЂ Р С‘Р С‘
    # =========================================================

    async def accept(
        self,
        *,
        item_id: int,
        operator_id: int,
    ) -> OrderItem:
        """
        NEW РІвЂ вЂ™ ACCEPTED

        - Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚ Р С—РЎР‚Р С‘Р Р…Р С‘Р СР В°Р ВµРЎвЂљ Р С—Р С•Р В·Р С‘РЎвЂ Р С‘РЎР‹
        - РЎвЂћР С‘Р С”РЎРѓР С‘РЎР‚РЎС“Р ВµРЎвЂљРЎРѓРЎРЏ operator_id
        """

        item = await self.get_by_id(
            item_id=item_id,
            for_update=True,
        )

        if not item:
            raise NotFoundError("OrderItem not found")

        if item.status != OrderItemStatus.NEW:
            raise InvalidStateError("Invalid state transition")

        item.status = OrderItemStatus.ACCEPTED
        item.operator_id = operator_id
        item.accepted_at = datetime.utcnow()

        await self.session.flush()
        return item

    async def mark_paid(
        self,
        *,
        item_id: int,
    ) -> OrderItem:
        """
        ACCEPTED РІвЂ вЂ™ PAID

        - Р Р†РЎвЂ№Р В·РЎвЂ№Р Р†Р В°Р ВµРЎвЂљРЎРѓРЎРЏ Р С—Р С•РЎРѓР В»Р Вµ Р С—Р С•Р Т‘РЎвЂљР Р†Р ВµРЎР‚Р В¶Р Т‘Р ВµР Р…Р С‘РЎРЏ Р С•Р С—Р В»Р В°РЎвЂљРЎвЂ№
        - Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚ Р С•РЎРѓРЎвЂљР В°РЎвЂРЎвЂљРЎРѓРЎРЏ РЎвЂљР ВµР С Р В¶Р Вµ
        """

        item = await self.get_by_id(
            item_id=item_id,
            for_update=True,
        )

        if not item:
            raise NotFoundError("OrderItem not found")

        if item.status != OrderItemStatus.ACCEPTED:
            raise InvalidStateError("Invalid state transition")

        item.status = OrderItemStatus.PAID
        item.paid_at = datetime.utcnow()

        await self.session.flush()
        return item

    async def complete(
        self,
        *,
        item_id: int,
    ) -> OrderItem:
        """
        PAID РІвЂ вЂ™ DONE

        РІСњвЂ” Р С™Р В Р ВР СћР ВР В§Р вЂўР РЋР С™Р В Р вЂ™Р С’Р вЂ“Р СњР С›:
        ------------------------------------------------
        DONE = РЎвЂљР С•Р Р†Р В°РЎР‚ РЎРѓР С—Р С‘РЎРѓР В°Р Р… Р В»Р С•Р С–Р С‘РЎвЂЎР ВµРЎРѓР С”Р С‘.
        Р СњР ВР С™Р С’Р С™Р С›Р вЂњР С› Р Т‘Р С•Р С—Р С•Р В»Р Р…Р С‘РЎвЂљР ВµР В»РЎРЉР Р…Р С•Р С–Р С• writeoff Р Р…Р Вµ РЎвЂљРЎР‚Р ВµР В±РЎС“Р ВµРЎвЂљРЎРѓРЎРЏ.

        Р вЂ™РЎРѓРЎвЂ, РЎвЂЎРЎвЂљР С• Р С—РЎР‚Р С•Р С‘РЎРѓРЎвЂ¦Р С•Р Т‘Р С‘РЎвЂљ Р Т‘Р В°Р В»РЎРЉРЎв‚¬Р Вµ (Р В·Р В°РЎР‚Р С—Р В»Р В°РЎвЂљР В°, РЎС“Р Р†Р ВµР Т‘Р С•Р СР В»Р ВµР Р…Р С‘РЎРЏ),
        РЎРѓРЎвЂљРЎР‚Р С•Р С‘РЎвЂљРЎРѓРЎРЏ Р С•РЎвЂљ РЎРЊРЎвЂљР С•Р С–Р С• РЎвЂћР В°Р С”РЎвЂљР В°.
        """

        item = await self.get_by_id(
            item_id=item_id,
            for_update=True,
        )

        if not item:
            raise NotFoundError("OrderItem not found")

        if item.status != OrderItemStatus.PAID:
            raise InvalidStateError("Invalid state transition")

        item.status = OrderItemStatus.DONE
        item.completed_at = datetime.utcnow()

        await self.session.flush()
        return item

    # =========================================================
    # OPERATOR DASHBOARD
    # =========================================================

    async def get_active_for_operator(
        self,
        *,
        operator_id: int,
    ) -> list[OrderItem]:
        """
        Р вЂ™Р С•Р В·Р Р†РЎР‚Р В°РЎвЂ°Р В°Р ВµРЎвЂљ Р В°Р С”РЎвЂљР С‘Р Р†Р Р…РЎвЂ№Р Вµ Р С—Р С•Р В·Р С‘РЎвЂ Р С‘Р С‘ Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚Р В°.

        Р ВРЎРѓР С—Р С•Р В»РЎРЉР В·РЎС“Р ВµРЎвЂљРЎРѓРЎРЏ Р Т‘Р В»РЎРЏ:
        - Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚РЎРѓР С”Р С•Р С–Р С• РЎРЊР С”РЎР‚Р В°Р Р…Р В°
        - SLA / РЎвЂљР В°Р в„–Р СР С‘Р Р…Р С–Р С•Р Р†
        - Р С”Р С•Р Р…РЎвЂљРЎР‚Р С•Р В»РЎРЏ Р В·Р В°Р С–РЎР‚РЎС“Р В·Р С”Р С‘

        DONE РЎРѓРЎР‹Р Т‘Р В° Р СњР вЂў Р С—Р С•Р С—Р В°Р Т‘Р В°РЎР‹РЎвЂљ.
        """

        res = await self.session.execute(
            select(OrderItem)
            .where(
                OrderItem.operator_id == operator_id,
                OrderItem.status.in_(
                    (
                        OrderItemStatus.ACCEPTED,
                        OrderItemStatus.PAID,
                    )
                ),
            )
            .order_by(OrderItem.accepted_at)
        )
        return list(res.scalars())

