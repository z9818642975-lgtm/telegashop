from bot_refactored.models.order import OrderStatus


class OrderStateError(Exception):
    pass


class OrderDomain:
    ALLOWED = {
        OrderStatus.NEW: {OrderStatus.ACCEPTED},
        OrderStatus.ACCEPTED: {OrderStatus.PAID},
        OrderStatus.PAID: {OrderStatus.DONE},
        OrderStatus.DONE: set(),
    }

    def __init__(self, status: OrderStatus):
        self.status = status

    def can_transition(self, to: OrderStatus) -> None:
        if to not in self.ALLOWED[self.status]:
            raise OrderStateError(f"invalid transition {self.status} -> {to}")

