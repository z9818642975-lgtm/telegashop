# bot/fsm/operator_shift_fsm.py
from aiogram.fsm.state import State, StatesGroup


class OperatorShiftFSM(StatesGroup):
    enter_address = State()
    confirm = State()
    pickup_address = State()


