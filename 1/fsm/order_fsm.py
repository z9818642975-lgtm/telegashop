# -*- coding: utf-8 -*-
# bot/fsm/order.py
# bot/fsm/order.py


from aiogram.fsm.state import StatesGroup, State








class OrderFSM(StatesGroup):


    delivery_type = State()


    address = State()


    payment_bank = State()


    wait_check = State()





