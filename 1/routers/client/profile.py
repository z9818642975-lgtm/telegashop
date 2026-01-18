# bot/routers/client/profile.py
from aiogram import Router, types

# bot/routers/client/profile.py
from aiogram import Router, types





router = Router()





@router.message(lambda m: m.text == "РЎР‚РЎСџРІР‚ВР’В¤ Р В РЎСџР РЋР вЂљР В РЎвЂўР РЋРІР‚С›Р В РЎвЂР В Р’В»Р РЋР Р‰")


async def profile(message: types.Message):


    await message.answer("РЎР‚РЎСџРІР‚ВР’В¤ Р В РЎСџР РЋР вЂљР В РЎвЂўР РЋРІР‚С›Р В РЎвЂР В Р’В»Р РЋР Р‰\nР В Р Р‹Р РЋРІР‚С™Р В Р’В°Р РЋРІР‚С™Р РЋРЎвЂњР РЋР С“: Р В РЎвЂќР В Р’В»Р В РЎвЂР В Р’ВµР В Р вЂ¦Р РЋРІР‚С™")





