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








# Тайминги (минуты)


FIRST_WARN_MIN = 15


SECOND_WARN_MIN = 17   # +2


FINAL_WARN_MIN = 20    # +3








class OperatorOnlineService:


    """


    Сервис онлайн-контроля операторов.





    Контролирует АКТИВНЫЕ СМЕНЫ (OperatorShift),


    проверяет last_seen_at оператора и:


      - шлёт предупреждения


      - автоматически завершает смену при оффлайне


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


                # защита от падения сервиса


                print(f"[OperatorOnlineService] error: {e}")


            await asyncio.sleep(self.interval_sec)





    async def _check(self):


        now = datetime.utcnow()





        async with self.session_maker() as session:


            dao = WarehousesDAO(session)





            # 🔑 1. Получаем АКТИВНЫЕ СМЕНЫ


            shifts = await session.scalars(


                select(OperatorShift)


                .where(OperatorShift.ended_at.is_(None))


            )


            shifts = shifts.all()





            for shift in shifts:


                operator_id = shift.operator_id





                # 🔑 2. Получаем last_seen оператора


                last_seen_at = await dao.get_operator_last_seen(operator_id)


                if not last_seen_at:


                    continue





                delta_min = (now - last_seen_at).total_seconds() / 60





                # 15 минут — первое предупреждение


                if FIRST_WARN_MIN <= delta_min < SECOND_WARN_MIN:


                    await self._notify_operator(


                        operator_id,


                        "⚠️ Вы неактивны 15 минут.\nНажмите «Я на месте», иначе смена будет завершена.",


                    )





                # +2 минуты — второе предупреждение


                elif SECOND_WARN_MIN <= delta_min < FINAL_WARN_MIN:


                    await self._notify_operator(


                        operator_id,


                        "⚠️ Вы всё ещё неактивны.\nНажмите «Я на месте» прямо сейчас.",


                    )





                # +3 минуты — авто-завершение смены


                elif delta_min >= FINAL_WARN_MIN:


                    await dao.stop_operator_shift(operator_id)


                    await session.commit()





                    await self._notify_operator(


                        operator_id,


                        "❌ Вы были сняты со смены из-за неактивности.",


                    )





                    if self.admin_notify:


                        self.admin_notify(


                            f"Оператор {operator_id} снят со смены (оффлайн)"


                        )





    async def _notify_operator(self, operator_id: int, text: str):


        try:


            await self.bot.send_message(operator_id, text)


        except Exception:


            # оператор заблокировал бота или недоступен


            pass





