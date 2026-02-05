# bot/routers/admin/__init__.py
from aiogram import Router

from .banks import router as banks_router
from .menu import router as menu_router
from .operators import router as operators_router
from .orders import router as orders_router
from .products import router as products_router
from .salary import router as salary_router
from .statistics import router as statistics_router
from .warehouses import router as warehouses_router

router = Router(name="admin")

router.include_router(menu_router)
router.include_router(products_router)
router.include_router(warehouses_router)
router.include_router(operators_router)
router.include_router(orders_router)
router.include_router(salary_router)
router.include_router(banks_router)
router.include_router(statistics_router)

