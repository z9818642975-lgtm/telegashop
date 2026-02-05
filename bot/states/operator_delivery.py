# bot/states/operator_delivery.py
from aiogram.fsm.state import State, StatesGroup


class OperatorDeliveryFSM(StatesGroup):
    comment = State()
    photo = State()
