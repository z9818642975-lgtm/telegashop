# bot/filters/role.py
from aiogram.filters import BaseFilter

# bot/filters/role.py
from aiogram.filters import BaseFilter


from aiogram.types import Message, CallbackQuery





from bot.models.enums import UserRole








class RoleFilter(BaseFilter):


    def __init__(self, role: UserRole):


        self.role = role





    async def __call__(self, event: Message | CallbackQuery, **kwargs) -> bool:


        user = kwargs.get("user")





        # РІСњРЉ Р СњР вЂўР вЂєР В¬Р вЂ”Р Р‡ Р С—РЎС“РЎРѓР С”Р В°РЎвЂљРЎРЉ user=None Р Р…Р С‘Р С”РЎС“Р Т‘Р В°, Р С”РЎР‚Р С•Р СР Вµ /start


        if user is None:


            return False





        return user.role == self.role





