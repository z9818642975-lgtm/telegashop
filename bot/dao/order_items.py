# bot/dao/order_items.py
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.models.order_item import OrderItem
from bot.models.enums import OrderItemStatus
from bot.exceptions import NotFoundError, InvalidStateError


class OrderItemDAO:
    """
    DAO для OrderItem — КЛЮЧЕВАЯ бизнес-единица проекта.

    Архитектурные принципы (ЗАФИКСИРОВАНО):
    ------------------------------------------------
    1) OrderItem — атомарная единица работы оператора
    2) OrderItem.operator_id — владелец позиции
    3) OrderItem.status — источник истины по жизненному циклу
    4) DONE = товар списан логически
    5) Warehouse / остатки / движения — НЕ часть этой логики
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    # =========================================================
    # CLIENT FLOW
    # Добавление / увеличение позиции в корзине
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
        Добавляет товар в заказ или увеличивает количество,
        если позиция уже есть в корзине.

        Используется ТОЛЬКО на клиентском этапе (до оператора).
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
        Получение OrderItem по ID.

        for_update=True используется:
        - в операторских сценариях
        - для защиты от гонок статусов
        """
        return await self.session.get(
            OrderItem,
            item_id,
            with_for_update=for_update,
        )

    # =========================================================
    # OPERATOR FLOW
    # Жизненный цикл позиции
    # =========================================================

    async def accept(
        self,
        *,
        item_id: int,
        operator_id: int,
    ) -> OrderItem:
        """
        NEW → ACCEPTED

        - оператор принимает позицию
        - фиксируется operator_id
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
        ACCEPTED → PAID

        - вызывается после подтверждения оплаты
        - оператор остаётся тем же
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
        PAID → DONE

        ❗ КРИТИЧЕСКИ ВАЖНО:
        ------------------------------------------------
        DONE = товар списан логически.
        НИКАКОГО дополнительного writeoff не требуется.

        Всё, что происходит дальше (зарплата, уведомления),
        строится от этого факта.
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
        Возвращает активные позиции оператора.

        Используется для:
        - операторского экрана
        - SLA / таймингов
        - контроля загрузки

        DONE сюда НЕ попадают.
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

