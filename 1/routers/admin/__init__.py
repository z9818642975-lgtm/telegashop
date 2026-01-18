from aiogram import Router
from aiogram import F

router = Router(name="admin")

# 🔒 ADMIN CALLBACK GUARD
router.callback_query.filter(F.data.startswith("admin:"))

from .admin import router as admin_router
from .products import router as products_router
from .operators import router as operators_router
from .warehouses import router as warehouses_router
from .reports import router as reports_router
from .audit import router as audit_router

router.include_router(admin_router)
router.include_router(products_router)
router.include_router(operators_router)
router.include_router(warehouses_router)
router.include_router(reports_router)
router.include_router(audit_router)

