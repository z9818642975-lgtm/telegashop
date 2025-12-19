from aiogram import Router
from .start import router as start_router
from .catalog import router as catalog_router
router = Router()
router.include_router(start_router)
router.include_router(catalog_router)
