from enum import Enum

class Role(str, Enum):
    CLIENT="CLIENT"
    OPERATOR="OPERATOR"
    ADMIN="ADMIN"

class OrderStatus(str, Enum):
    NEW="NEW"
    WAIT_PAYMENT="WAIT_PAYMENT"
    PAID="PAID"
    IN_PROGRESS="IN_PROGRESS"
    DONE="DONE"
    WAIT_OPERATOR="WAIT_OPERATOR"

class ReservationStatus(str, Enum):
    RESERVED="RESERVED"
    USED="USED"
    RELEASED="RELEASED"
