from enum import StrEnum, auto


class UserRole(StrEnum):
    ADMIN = auto()
    OPERATOR = auto()
    CLIENT = auto()


class OrderStatus(StrEnum):
    NEW = auto()                 # корзина
    WAITING_PAYMENT = auto()     # ожидаем оплату
    PAYMENT_SUBMITTED = auto()   # чек отправлен
    ASSEMBLING = auto()          # оператор собирает
    READY = auto()               # оператор загрузил фото + описание
    SENT = auto()                # доставка отправлена
    PICKED_UP = auto()           # самовывоз забран
    DONE = auto()
    CANCELLED = auto()


class OrderItemStatus(StrEnum):
    NEW = auto()
    ACCEPTED = auto()
    PAID = auto()
    DONE = auto()
    CANCELLED = auto()


class PaymentMethod(StrEnum):
    SBP = auto()
    BANK = auto()


class PaymentStatus(StrEnum):
    NEW = auto()
    SUBMITTED = auto()
    CONFIRMED = auto()
    REJECTED = auto()

