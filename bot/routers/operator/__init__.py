from aiogram import Router

from .shifts import router as shifts_router

router = Router(name="operator")
router.include_router(shifts_router)
