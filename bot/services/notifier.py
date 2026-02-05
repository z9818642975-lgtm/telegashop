# bot/services/notifier.py
from __future__ import annotations

from typing import Iterable, Optional

from aiogram import Bot


class Notifier:
    """
    Централизованный сервис уведомлений.

    Используется:
    - operator_shift_watcher
    - orders lifecycle
    - admin / operator события
    - payment / SLA / system alerts

    Канал доставки сейчас: Telegram
    В будущем можно добавить: лог, webhook, email
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    # =========================================================
    # LOW LEVEL
    # =========================================================

    async def send(
        self,
        chat_id: int,
        text: str,
        *,
        silent: bool = False,
    ) -> None:
        await self.bot.send_message(
            chat_id=chat_id,
            text=text,
            disable_notification=silent,
        )

    async def broadcast(
        self,
        chat_ids: Iterable[int],
        text: str,
        *,
        silent: bool = False,
    ) -> None:
        for cid in chat_ids:
            try:
                await self.send(cid, text, silent=silent)
            except Exception:
                # намеренно глушим — уведомления не должны ронять систему
                pass

    # =========================================================
    # CLIENT
    # =========================================================

    async def notify_client_order_created(
        self,
        client_tg_id: int,
        order_id: int,
    ) -> None:
        await self.send(
            client_tg_id,
            f"🛒 Заказ #{order_id} создан.\nПерейдите к оплате.",
        )

    async def notify_client_payment_received(
        self,
        client_tg_id: int,
        order_id: int,
    ) -> None:
        await self.send(
            client_tg_id,
            f"💰 Чек по заказу #{order_id} получен.\nОжидает проверки оператором.",
        )

    async def notify_client_payment_confirmed(
        self,
        client_tg_id: int,
        order_id: int,
    ) -> None:
        await self.send(
            client_tg_id,
            f"✅ Оплата по заказу #{order_id} подтверждена.\nЗаказ принят в работу.",
        )

    async def notify_client_order_ready(
        self,
        client_tg_id: int,
        order_id: int,
    ) -> None:
        await self.send(
            client_tg_id,
            f"📦 Заказ #{order_id} готов к выдаче.",
        )

    async def notify_client_order_cancelled(
        self,
        client_tg_id: int,
        order_id: int,
        reason: Optional[str] = None,
    ) -> None:
        text = f"❌ Заказ #{order_id} отменён."
        if reason:
            text += f"\nПричина: {reason}"
        await self.send(client_tg_id, text)

    # =========================================================
    # OPERATOR
    # =========================================================

    async def notify_operator_shift_started(
        self,
        operator_tg_id: int,
    ) -> None:
        await self.send(
            operator_tg_id,
            "🟢 Смена начата.\nОжидайте заказы.",
        )

    async def notify_operator_shift_ending(
        self,
        operator_tg_id: int,
        minutes_left: int,
    ) -> None:
        await self.send(
            operator_tg_id,
            f"⚠️ До окончания смены осталось {minutes_left} мин.",
            silent=True,
        )

    async def notify_operator_shift_closed(
        self,
        operator_tg_id: int,
    ) -> None:
        await self.send(
            operator_tg_id,
            "⛔ Смена завершена.",
        )

    async def notify_operator_new_order(
        self,
        operator_tg_id: int,
        order_id: int,
    ) -> None:
        await self.send(
            operator_tg_id,
            f"📦 Новый заказ #{order_id} принят в работу.",
        )

    async def notify_operator_payment_check_required(
        self,
        operator_tg_id: int,
        order_id: int,
    ) -> None:
        await self.send(
            operator_tg_id,
            f"💰 Требуется проверка оплаты по заказу #{order_id}.",
        )

    async def notify_operator_sla_expired(
        self,
        operator_tg_id: int,
        order_id: int,
    ) -> None:
        await self.send(
            operator_tg_id,
            f"⏱ SLA по заказу #{order_id} истёк!",
        )

    # =========================================================
    # ADMIN
    # =========================================================

    async def notify_admin_new_order(
        self,
        admin_tg_id: int,
        order_id: int,
    ) -> None:
        await self.send(
            admin_tg_id,
            f"📋 Новый заказ #{order_id}.",
        )

    async def notify_admin_payment_issue(
        self,
        admin_tg_id: int,
        order_id: int,
    ) -> None:
        await self.send(
            admin_tg_id,
            f"⚠️ Проблема с оплатой по заказу #{order_id}.",
        )

    async def notify_admin_operator_payout_requested(
        self,
        admin_tg_id: int,
        operator_tg_id: int,
    ) -> None:
        await self.send(
            admin_tg_id,
            f"💸 Оператор {operator_tg_id} запросил выплату.",
        )

    async def notify_admin_system_alert(
        self,
        admin_tg_id: int,
        text: str,
    ) -> None:
        await self.send(
            admin_tg_id,
            f"🚨 SYSTEM ALERT:\n{text}",
        )