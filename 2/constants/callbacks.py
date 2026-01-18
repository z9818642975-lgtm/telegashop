class CB:
    # ============================
    # CLIENT — CART / CATALOG
    # ============================

    CATALOG = "catalog"

    CART_OPEN = "cart:open"
    CART_CHECKOUT = "cart:checkout"
    CART_CLEAR = "cart:clear"

    PRODUCT = "product:{id}"
    QTY = "qty:{id}:{qty}"

    BACK_CATALOG = "back:catalog"
    BACK_PRODUCT = "back:product:{id}"   # ✅ ОБЯЗАТЕЛЬНО

    ITEM_REMOVE = "item:remove:{id}"

    # ============================
    # CLIENT — CHECKOUT
    # ============================

    DELIVERY_PICKUP = "delivery:pickup"
    DELIVERY_COURIER = "delivery:courier"

    PAYMENT_CASH = "payment:cash"
    PAYMENT_CARD = "payment:card"

    # ============================
    # OPERATOR — SHIFT
    # ============================

    OP_SHIFT_STOP = "op:shift:stop"
    OP_SHIFT_EDIT_ADDRESS = "op:shift:edit"

    OP_ALIVE = "op:alive"

    # ============================
    # OPERATOR — ORDERS
    # ============================

    OP_CHECK_ACCEPT = "op:check:accept:{order_id}"

    OP_ORDER_READY = "op:order:ready:{order_id}"
    OP_ORDER_SENT = "op:order:sent:{order_id}"

