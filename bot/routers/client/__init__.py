from aiogram import Router

from .catalog import router as catalog_router
from .quantity import router as quantity_router
from .cart import router as cart_router
from .checkout import router as checkout_router
from .payment import router as payment_router
from .menu import router as menu_router

router = Router(name="client")

# Специфичные пользовательские действия
router.include_router(catalog_router)
router.include_router(quantity_router)
router.include_router(cart_router)
router.include_router(checkout_router)
router.include_router(payment_router)

# Главное меню — В КОНЦЕ
router.include_router(menu_router)

__all__ = ["router"]

