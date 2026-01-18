# bot/routers/admin/stats.py
# ============================================================

# bot/routers/admin/stats.py
# ============================================================


# bot/routers/admin/stats.py


# ============================================================





from aiogram import Router, F


from aiogram.types import CallbackQuery


from sqlalchemy.ext.asyncio import AsyncSession





from bot.dao.statistics import StatisticsDAO





router = Router(name="admin_stats")








# ------------------------------------------------------------


# СВОДКА


# ------------------------------------------------------------





@router.callback_query(F.data == "admin:stats:summary")


async def admin_stats_summary(


    callback: CallbackQuery,


    session: AsyncSession,


) -> None:


    dao = StatisticsDAO(session)


    data = await dao.today_summary()





    await callback.message.edit_text(


        "📊 <b>Статистика за сегодня</b>\n\n"


        f"📦 Заказов: {data['orders_total']}\n"


        f"✅ Оплачено: {data['orders_paid']}\n"


        f"💰 Оборот: {data['revenue']} ₽\n"


        f"🧾 Средний чек: {data['avg_check']} ₽\n\n"


        f"👷 Операторов всего: {data['operators_total']}\n"


        f"🟢 Активных смен: {data['active_shifts']}\n\n"


        f"💸 Начислено зарплат: {data['salary_today']} ₽",


        parse_mode="HTML",


    )


    await callback.answer()








# ------------------------------------------------------------


# ЗАКАЗЫ: СТАТУСЫ + ТАЙМИНГИ


# ------------------------------------------------------------





@router.callback_query(F.data == "admin:stats:orders")


async def admin_stats_orders(


    callback: CallbackQuery,


    session: AsyncSession,


) -> None:


    dao = StatisticsDAO(session)





    statuses = await dao.orders_by_status_today()


    timings = await dao.order_timings_today()





    text = "📦 <b>Заказы за сегодня</b>\n\n"





    for status, count in statuses.items():


        text += f"{status}: {count}\n"





    text += (


        f"\n⏱ <b>Среднее время</b>\n"


        f"→ до оплаты: {timings['to_paid_min']} мин\n"


        f"→ до отправки: {timings['to_sent_min']} мин"


    )





    await callback.message.edit_text(text, parse_mode="HTML")


    await callback.answer()








# ------------------------------------------------------------


# ОПЕРАТОРЫ: SLA


# ------------------------------------------------------------





@router.callback_query(F.data == "admin:stats:operators")


async def admin_stats_operators(


    callback: CallbackQuery,


    session: AsyncSession,


) -> None:


    dao = StatisticsDAO(session)


    data = await dao.operators_sla_today()





    await callback.message.edit_text(


        "👷 <b>Операторы за сегодня</b>\n\n"


        f"🟢 Смен открыто: {data['shifts_total']}\n"


        f"✅ Смен закрыто: {data['shifts_closed']}\n"


        f"🚫 Выкинуто со смены: {data['kicked']}",


        parse_mode="HTML",


    )


    await callback.answer()








# ------------------------------------------------------------


# ВЫРУЧКА: БАНК vs СБП


# ------------------------------------------------------------





@router.callback_query(F.data == "admin:stats:revenue")


async def admin_stats_revenue(


    callback: CallbackQuery,


    session: AsyncSession,


) -> None:


    dao = StatisticsDAO(session)


    data = await dao.revenue_by_method_today()





    text = "💰 <b>Выручка за сегодня</b>\n\n"


    for method, amount in data.items():


        text += f"{method}: {amount} ₽\n"





    await callback.message.edit_text(text, parse_mode="HTML")


    await callback.answer()





