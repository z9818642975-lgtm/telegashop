# -*- coding: utf-8 -*- order_fsm.py
# bot/fsm/1/order_fsm.py
# bot/fsm/1/order_fsm.py


from aiogram.fsm.state import StatesGroup, State








class OrderFSM(StatesGroup):


    select_product = State()


    select_quantity = State()


    select_delivery_type = State()


    select_delivery_price = State()


    select_bank = State()


    confirm_payment = State()





