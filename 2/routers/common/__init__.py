# bot/routers/common/__init__.py
from aiogram import Router

# bot/routers/common/__init__.py
from aiogram import Router


from .back import router as back_router





router = Router(name="common")


router.include_router(back_router)





