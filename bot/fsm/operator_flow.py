# bot/fsm/operator_flow.py
from aiogram.fsm.state import State, StatesGroup


class OperatorFlow(StatesGroup):
    enter_pickup_address = State()
    confirm_shift = State()

