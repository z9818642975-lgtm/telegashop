from aiogram import Router
from aiogram.types import Message
from bot.config import settings

router = Router(name="chat")

# ❌ DISABLED (dangerous): router.message()
async def relay(message: Message):
    # РЎС“Р С—РЎР‚Р С•РЎвЂ°РЎвЂР Р…Р Р…РЎвЂ№Р в„– Р С—РЎР‚Р С•Р С”РЎРѓР С‘-РЎвЂЎР В°РЎвЂљ
    if message.reply_to_message:
        await message.answer("СЂСџвЂ™В¬ Р РЋР С•Р С•Р В±РЎвЂ°Р ВµР Р…Р С‘Р Вµ Р С—Р ВµРЎР‚Р ВµР Т‘Р В°Р Р…Р С• Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚РЎС“")

