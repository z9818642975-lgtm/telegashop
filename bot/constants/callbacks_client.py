from aiogram.filters.callback_data import CallbackData

# === MENU ===
class CatalogOpen(CallbackData, prefix="catalog_open"):
    pass


class ClientCartOpen(CallbackData, prefix="cart_open"):
    pass


class ClientProfileOpen(CallbackData, prefix="profile_open"):
    pass


class ClientFaqOpen(CallbackData, prefix="faq_open"):
    pass


class ClientSupportOpen(CallbackData, prefix="support_open"):
    pass


# === CATALOG ===
class ProductOpen(CallbackData, prefix="product_open"):
    product_id: int


class ClientItemQty(CallbackData, prefix="item_qty"):
    item_id: int
    qty: int


# === DELIVERY ===
class ClientDeliveryPickup(CallbackData, prefix="delivery_pickup"):
    pass


class ClientDeliveryCourier(CallbackData, prefix="delivery_courier"):
    pass


# === PAYMENT ===
class ClientPayBank(CallbackData, prefix="pay_bank"):
    bank_id: int


class ClientPaySBP(CallbackData, prefix="pay_sbp"):
    pass


class ClientPaymentCancel(CallbackData, prefix="pay_cancel"):
    pass
