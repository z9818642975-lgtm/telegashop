from aiogram import Router
from .start import router as start_router
from .shift import router as shift_router
router = Router()
router.include_router(start_router)
router.include_router(shift_router)
