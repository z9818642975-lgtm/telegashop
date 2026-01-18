# bot/services/operator_online.py
#C:\Users\1\project\bot\services\operator_online.py

# bot/services/operator_online.py
#C:\Users\1\project\bot\services\operator_online.py


import asyncio


from datetime import datetime


from typing import Callable





from aiogram import Bot


from sqlalchemy import select


from sqlalchemy.ext.asyncio import async_sessionmaker





from bot.models.operator_shift import OperatorShift


from bot.dao.warehouses_dao import WarehousesDAO








# Р СћР В°Р в„–Р СР С‘Р Р…Р С–Р С‘ (Р СР С‘Р Р…РЎС“РЎвЂљРЎвЂ№)


FIRST_WARN_MIN = 15


SECOND_WARN_MIN = 17   # +2


FINAL_WARN_MIN = 20    # +3








class OperatorOnlineService:


    """


    Р РЋР ВµРЎР‚Р Р†Р С‘РЎРѓ Р С•Р Р…Р В»Р В°Р в„–Р Р…-Р С”Р С•Р Р…РЎвЂљРЎР‚Р С•Р В»РЎРЏ Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚Р С•Р Р†.





    Р С™Р С•Р Р…РЎвЂљРЎР‚Р С•Р В»Р С‘РЎР‚РЎС“Р ВµРЎвЂљ Р С’Р С™Р СћР ВР вЂ™Р СњР В«Р вЂў Р РЋР СљР вЂўР СњР В« (OperatorShift),


    Р С—РЎР‚Р С•Р Р†Р ВµРЎР‚РЎРЏР ВµРЎвЂљ last_seen_at Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚Р В° Р С‘:


      - РЎв‚¬Р В»РЎвЂРЎвЂљ Р С—РЎР‚Р ВµР Т‘РЎС“Р С—РЎР‚Р ВµР В¶Р Т‘Р ВµР Р…Р С‘РЎРЏ


      - Р В°Р Р†РЎвЂљР С•Р СР В°РЎвЂљР С‘РЎвЂЎР ВµРЎРѓР С”Р С‘ Р В·Р В°Р Р†Р ВµРЎР‚РЎв‚¬Р В°Р ВµРЎвЂљ РЎРѓР СР ВµР Р…РЎС“ Р С—РЎР‚Р С‘ Р С•РЎвЂћРЎвЂћР В»Р В°Р в„–Р Р…Р Вµ


    """





    def __init__(


        self,


        bot: Bot,


        session_maker: async_sessionmaker,


        admin_notify: Callable[[str], None] | None = None,


        interval_sec: int = 60,


    ):


        self.bot = bot


        self.session_maker = session_maker


        self.admin_notify = admin_notify


        self.interval_sec = interval_sec


        self._task: asyncio.Task | None = None





    async def start(self):


        if self._task:


            return


        self._task = asyncio.create_task(self._loop())





    async def _loop(self):


        while True:


            try:


                await self._check()


            except Exception as e:


                # Р В·Р В°РЎвЂ°Р С‘РЎвЂљР В° Р С•РЎвЂљ Р С—Р В°Р Т‘Р ВµР Р…Р С‘РЎРЏ РЎРѓР ВµРЎР‚Р Р†Р С‘РЎРѓР В°


                print(f"[OperatorOnlineService] error: {e}")


            await asyncio.sleep(self.interval_sec)





    async def _check(self):


        now = datetime.utcnow()





        async with self.session_maker() as session:


            dao = WarehousesDAO(session)





            # СЂСџвЂќвЂ 1. Р СџР С•Р В»РЎС“РЎвЂЎР В°Р ВµР С Р С’Р С™Р СћР ВР вЂ™Р СњР В«Р вЂў Р РЋР СљР вЂўР СњР В«


            shifts = await session.scalars(


                select(OperatorShift)


                .where(OperatorShift.ended_at.is_(None))


            )


            shifts = shifts.all()





            for shift in shifts:


                operator_id = shift.operator_id





                # СЂСџвЂќвЂ 2. Р СџР С•Р В»РЎС“РЎвЂЎР В°Р ВµР С last_seen Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚Р В°


                last_seen_at = await dao.get_operator_last_seen(operator_id)


                if not last_seen_at:


                    continue





                delta_min = (now - last_seen_at).total_seconds() / 60





                # 15 Р СР С‘Р Р…РЎС“РЎвЂљ РІР‚вЂќ Р С—Р ВµРЎР‚Р Р†Р С•Р Вµ Р С—РЎР‚Р ВµР Т‘РЎС“Р С—РЎР‚Р ВµР В¶Р Т‘Р ВµР Р…Р С‘Р Вµ


                if FIRST_WARN_MIN <= delta_min < SECOND_WARN_MIN:


                    await self._notify_operator(


                        operator_id,


                        "РІС™В РїС‘РЏ Р вЂ™РЎвЂ№ Р Р…Р ВµР В°Р С”РЎвЂљР С‘Р Р†Р Р…РЎвЂ№ 15 Р СР С‘Р Р…РЎС“РЎвЂљ.\nР СњР В°Р В¶Р СР С‘РЎвЂљР Вµ Р’В«Р Р‡ Р Р…Р В° Р СР ВµРЎРѓРЎвЂљР ВµР’В», Р С‘Р Р…Р В°РЎвЂЎР Вµ РЎРѓР СР ВµР Р…Р В° Р В±РЎС“Р Т‘Р ВµРЎвЂљ Р В·Р В°Р Р†Р ВµРЎР‚РЎв‚¬Р ВµР Р…Р В°.",


                    )





                # +2 Р СР С‘Р Р…РЎС“РЎвЂљРЎвЂ№ РІР‚вЂќ Р Р†РЎвЂљР С•РЎР‚Р С•Р Вµ Р С—РЎР‚Р ВµР Т‘РЎС“Р С—РЎР‚Р ВµР В¶Р Т‘Р ВµР Р…Р С‘Р Вµ


                elif SECOND_WARN_MIN <= delta_min < FINAL_WARN_MIN:


                    await self._notify_operator(


                        operator_id,


                        "РІС™В РїС‘РЏ Р вЂ™РЎвЂ№ Р Р†РЎРѓРЎвЂ Р ВµРЎвЂ°РЎвЂ Р Р…Р ВµР В°Р С”РЎвЂљР С‘Р Р†Р Р…РЎвЂ№.\nР СњР В°Р В¶Р СР С‘РЎвЂљР Вµ Р’В«Р Р‡ Р Р…Р В° Р СР ВµРЎРѓРЎвЂљР ВµР’В» Р С—РЎР‚РЎРЏР СР С• РЎРѓР ВµР в„–РЎвЂЎР В°РЎРѓ.",


                    )





                # +3 Р СР С‘Р Р…РЎС“РЎвЂљРЎвЂ№ РІР‚вЂќ Р В°Р Р†РЎвЂљР С•-Р В·Р В°Р Р†Р ВµРЎР‚РЎв‚¬Р ВµР Р…Р С‘Р Вµ РЎРѓР СР ВµР Р…РЎвЂ№


                elif delta_min >= FINAL_WARN_MIN:


                    await dao.stop_operator_shift(operator_id)


                    await session.commit()





                    await self._notify_operator(


                        operator_id,


                        "РІСњРЉ Р вЂ™РЎвЂ№ Р В±РЎвЂ№Р В»Р С‘ РЎРѓР Р…РЎРЏРЎвЂљРЎвЂ№ РЎРѓР С• РЎРѓР СР ВµР Р…РЎвЂ№ Р С‘Р В·-Р В·Р В° Р Р…Р ВµР В°Р С”РЎвЂљР С‘Р Р†Р Р…Р С•РЎРѓРЎвЂљР С‘.",


                    )





                    if self.admin_notify:


                        self.admin_notify(


                            f"Р С›Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚ {operator_id} РЎРѓР Р…РЎРЏРЎвЂљ РЎРѓР С• РЎРѓР СР ВµР Р…РЎвЂ№ (Р С•РЎвЂћРЎвЂћР В»Р В°Р в„–Р Р…)"


                        )





    async def _notify_operator(self, operator_id: int, text: str):


        try:


            await self.bot.send_message(operator_id, text)


        except Exception:


            # Р С•Р С—Р ВµРЎР‚Р В°РЎвЂљР С•РЎР‚ Р В·Р В°Р В±Р В»Р С•Р С”Р С‘РЎР‚Р С•Р Р†Р В°Р В» Р В±Р С•РЎвЂљР В° Р С‘Р В»Р С‘ Р Р…Р ВµР Т‘Р С•РЎРѓРЎвЂљРЎС“Р С—Р ВµР Р…


            pass





