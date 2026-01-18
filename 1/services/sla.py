import asyncio
from datetime import timedelta

class SLAService:
    @staticmethod
    async def run(operator_id: int, notify):
        await asyncio.sleep(15 * 60)
        await notify(operator_id, "вЏ± Р’С‹ РЅРµР°РєС‚РёРІРЅС‹ 15 РјРёРЅСѓС‚")

        await asyncio.sleep(2 * 60)
        await notify(operator_id, "вљ пёЏ РЎРјРµРЅР° Р±СѓРґРµС‚ Р·Р°РєСЂС‹С‚Р° С‡РµСЂРµР· 3 РјРёРЅСѓС‚С‹")

        await asyncio.sleep(3 * 60)
        await notify(operator_id, "вќЊ РЎРјРµРЅР° Р°РІС‚РѕРјР°С‚РёС‡РµСЃРєРё Р·Р°РєСЂС‹С‚Р°")

