from bot_refactored.models.operator_shift import ShiftState


class ShiftStateError(Exception):
    pass


class OperatorShiftDomain:
    def __init__(self, state: ShiftState):
        self.state = state

    def can_open(self) -> None:
        if self.state == ShiftState.OPEN:
            raise ShiftStateError("shift already open")

    def can_close(self) -> None:
        if self.state == ShiftState.CLOSED:
            raise ShiftStateError("shift already closed")

