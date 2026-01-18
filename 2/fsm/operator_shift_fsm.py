from aiogram.fsm.state import StatesGroup, State

class OperatorShiftFSM(StatesGroup):
    enter_address = State()
    confirm = State()
    pickup_address = State()

