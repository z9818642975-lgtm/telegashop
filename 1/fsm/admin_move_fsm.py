# bot/fsm/admin_move_fsm.py

# bot/fsm/admin_move_fsm.py
# bot/fsm/admin_move_fsm.py


from aiogram.fsm.state import StatesGroup, State





class AdminMoveFSM(StatesGroup):


    from_warehouse = State()


    to_warehouse = State()


    product = State()


    qty = State()




