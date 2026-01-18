from aiogram import Router

from .shifts import router as shifts_router
from .pickup import router as pickup_router

router = Router(name="operator")

router.include_router(shifts_router)
router.include_router(pickup_router)

__all__ = ["router"]

