# bot/fsm/operator_flow.py
from aiogram.fsm.state import State, StatesGroup
    paid = State()
# bot/fsm/operator_flow.py
from aiogram.fsm.state import State, StatesGroup





class OperatorItemFSM(StatesGroup):


    idle = State()


    accepted = State()


    paid = State()


