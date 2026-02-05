# bot/routers/client/__init__.py
from aiogram import Router

from .cart import router as client_cart_router
from .catalog import router as client_catalog_router
from .checkout import router as client_checkout_router
from .menu import router as client_menu_router

router = Router(name="client")

router.include_router(client_menu_router)
router.include_router(client_catalog_router)
router.include_router(client_cart_router)
router.include_router(client_checkout_router)
