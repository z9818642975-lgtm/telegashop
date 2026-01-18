# bot/routers/common/__init__.py
from aiogram import Router

from .start import router as start_router
from .back import router as back_router

router = Router(name="common")

router.include_router(start_router)
router.include_router(back_router)

