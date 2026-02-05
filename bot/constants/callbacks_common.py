from aiogram.filters.callback_data import CallbackData


class BackToAdminMenu(CallbackData, prefix="back_admin"):
    pass


class BackToOperatorMenu(CallbackData, prefix="back_operator"):
    pass


class BackToClientMenu(CallbackData, prefix="back_client"):
    pass


class BackToAdminOrders(CallbackData, prefix="admin_orders_back"):
    pass


class BackCB(CallbackData, prefix="back"):
    target: str
