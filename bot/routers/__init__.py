# bot/routers/__init__.py
from aiogram import Router

from bot.routers.admin import router as admin_router
from bot.routers.client import router as client_router
from bot.routers.operator import router as operator_router
from bot.routers.start import router as start_router

# bot/routers/__init__.py
from .stub_handlers import router as stub_router

router = Router()

router.include_router(start_router)
router.include_router(client_router)
router.include_router(operator_router)
router.include_router(admin_router)
router.include_router(stub_router)

__all__ = ["router"]
