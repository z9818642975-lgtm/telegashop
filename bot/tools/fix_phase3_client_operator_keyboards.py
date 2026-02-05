from pathlib import Path

# =========================
# CLIENT KEYBOARDS — IMPORT FIXES
# =========================

CLIENT_IMPORTS = {
    "banks.py": [
        "from bot.constants.callbacks_client import ClientPayBank, ClientPaySBP",
    ],
    "cart.py": [
        "from bot.constants.callbacks_client import ClientItemRemove, ClientCartClear, ClientCartCheckout, CatalogOpen",
    ],
    "catalog.py": [
        "from bot.constants.callbacks_client import ClientWarehouseSelectCB",
    ],
    "common.py": [
        "from bot.constants.callbacks_client import ClientCartOpen",
    ],
    "delivery.py": [
        "from bot.constants.callbacks_client import ClientDeliveryPickup, ClientDeliveryCourier",
        "from bot.constants.callbacks_common import BackCB",
    ],
    "pickup.py": [
        "from bot.constants.callbacks_client import ClientCartOpen",
    ],
    "pickup_actions.py": [
        "from bot.constants.callbacks_common import ClientPaymentCancel",
    ],
}

CLIENT_DIR = Path("bot/keyboards/client")

for name, imports in CLIENT_IMPORTS.items():
    file = CLIENT_DIR / name
    if not file.exists():
        continue

    text = file.read_text(encoding="utf-8")
    for imp in imports:
        if imp not in text:
            text = imp + "\n" + text

    file.write_text(text, encoding="utf-8")
    print(f"[CLIENT FIX] {file}")


# =========================
# FIX BROKEN client checkout.py
# =========================

checkout = CLIENT_DIR / "checkout.py"
if checkout.exists():
    checkout.write_text(
        """from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.callbacks_client import (
    ClientCartOpen,
    ClientDeliveryCourier,
    ClientDeliveryPickup,
)


def client_checkout_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📍 Самовывоз",
                callback_data=ClientDeliveryPickup().pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="🚚 Курьер",
                callback_data=ClientDeliveryCourier().pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ В корзину",
                callback_data=ClientCartOpen().pack(),
            )
        ],
    ])
""",
        encoding="utf-8",
    )
    print("[CLIENT FIX] checkout.py rewritten")


# =========================
# FIX BROKEN client payment.py
# =========================

payment = CLIENT_DIR / "payment.py"
if payment.exists():
    payment.write_text(
        """from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.callbacks_client import (
    ClientPayBank,
    ClientPaySBP,
    ClientPaymentDone,
)
from bot.constants.callbacks_common import ClientPaymentCancel


def client_payment_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🏦 Сбер",
                callback_data=ClientPayBank(bank_id=1).pack(),
            ),
            InlineKeyboardButton(
                text="🏦 Т-Банк",
                callback_data=ClientPayBank(bank_id=2).pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="🏦 Альфа",
                callback_data=ClientPayBank(bank_id=3).pack(),
            ),
            InlineKeyboardButton(
                text="📱 СБП",
                callback_data=ClientPaySBP().pack(),
            ),
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=ClientPaymentCancel().pack(),
            )
        ],
    ])
""",
        encoding="utf-8",
    )
    print("[CLIENT FIX] payment.py rewritten")


# =========================
# OPERATOR KEYBOARDS — IMPORT FIXES
# =========================

OPERATOR_IMPORTS = {
    "heartbeat.py": [
        "from bot.constants.callbacks_operator import OperatorHeartbeatCB",
    ],
    "operator_order.py": [
        "from bot.constants.callbacks_operator import OperatorDeliverySentCB",
    ],
    "order_item.py": [
        "from bot.constants.callbacks_operator import OperatorCheckCB, OperatorDeliverySentCB",
    ],
    "orders.py": [
        "from bot.constants.callbacks_operator import OperatorOrdersCB",
    ],
    "salary.py": [
        "from bot.constants.callbacks_operator import OperatorSalaryStatsCB, OperatorSalaryPayoutCB",
    ],
    "statistics.py": [
        "from bot.constants.callbacks_operator import OperatorSalaryStatsCB",
    ],
}

OPERATOR_DIR = Path("bot/keyboards/operator")

for name, imports in OPERATOR_IMPORTS.items():
    file = OPERATOR_DIR / name
    if not file.exists():
        continue

    text = file.read_text(encoding="utf-8")
    for imp in imports:
        if imp not in text:
            text = imp + "\n" + text

    file.write_text(text, encoding="utf-8")
    print(f"[OPERATOR FIX] {file}")


# =========================
# FIX BROKEN operator/items.py
# =========================

items = OPERATOR_DIR / "items.py"
if items.exists():
    items.write_text(
        """from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants.callbacks_operator import OperatorCheckCB


def operator_items_kb(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="О 💰 Оплата прошла",
                callback_data=OperatorCheckCB(
                    order_id=order_id,
                    result="paid",
                ).pack(),
            )
        ],
        [
            InlineKeyboardButton(
                text="О ❌ Оплата не прошла",
                callback_data=OperatorCheckCB(
                    order_id=order_id,
                    result="failed",
                ).pack(),
            )
        ],
    ])
""",
        encoding="utf-8",
    )
    print("[OPERATOR FIX] items.py rewritten")

print("✅ PHASE 3 CLIENT + OPERATOR FIX COMPLETE")
