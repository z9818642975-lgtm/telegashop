from aiogram import Router

from bot.routers.common import router as common_router
from bot.routers.client import router as client_router
from bot.routers.operator import router as operator_router
from bot.routers.admin import router as admin_router

router = Router(name="root")

# порядок важен
router.include_router(common_router)
router.include_router(client_router)
router.include_router(operator_router)
router.include_router(admin_router)

