# bot/fsm/operator_pickup_fsm.py
from aiogram.fsm.state import State, StatesGroup


class OperatorPickupFSM(StatesGroup):
    comment = State()   # описание
    photo = State()     # фото


