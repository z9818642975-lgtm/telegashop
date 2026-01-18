from aiogram import Router
from aiogram import F

router = Router(name="client")

# 🔒 CLIENT CALLBACK GUARD
router.callback_query.filter(F.data.startswith("client:"))

from .menu import router as menu_router
from .catalog import router as catalog_router
from .cart import router as cart_router
from .checkout import router as checkout_router
from .payment_confirm import router as payment_confirm_router
from .pickup import router as pickup_router
from .pickup_timer import router as pickup_timer_router
from .profile import router as profile_router

router.include_router(menu_router)
router.include_router(catalog_router)
router.include_router(cart_router)
router.include_router(checkout_router)
router.include_router(payment_confirm_router)
router.include_router(pickup_router)
router.include_router(pickup_timer_router)
router.include_router(profile_router)

