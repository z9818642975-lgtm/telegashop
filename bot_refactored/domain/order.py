from bot_refactored.models.order import OrderStatus


class OrderStateError(Exception):
    pass


class OrderDomain:
    """
    Единственный источник правил переходов статусов заказа.
    НИКАКОЙ другой код не имеет права менять статус напрямую.
    """

    ALLOWED = {
        OrderStatus.NEW: {OrderStatus.ACCEPTED},
        OrderStatus.ACCEPTED: {OrderStatus.WAITING_CONFIRMATION},
        OrderStatus.WAITING_CONFIRMATION: {OrderStatus.PAID},
        OrderStatus.PAID: {OrderStatus.DONE},
        OrderStatus.DONE: set(),
    }

    def __init__(self, status: OrderStatus):
        self.status = status

    def can_transition(self, to: OrderStatus) -> None:
        if to not in self.ALLOWED[self.status]:
            raise OrderStateError(
                f"invalid transition {self.status} -> {to}"
            )

