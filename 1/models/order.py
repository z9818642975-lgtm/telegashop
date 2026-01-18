from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bot.models.base import Base
from bot.constants.order_status import OrderStatus  # в†ђ source of truth


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    operator_id: Mapped[int | None] = mapped_column(nullable=True)

    status: Mapped[str] = mapped_column(
        String,
        default=OrderStatus.DRAFT,
    )

    receipt_id: Mapped[str | None] = mapped_column(nullable=True)

    user = relationship("User")


# ------------------------------------------------------------------
# рџ”’ BACKWARD COMPATIBILITY (DO NOT REMOVE)
# ------------------------------------------------------------------
# РЎС‚Р°СЂС‹Р№ РєРѕРґ РјРѕР¶РµС‚ РґРµР»Р°С‚СЊ:
# from bot.models.order import OrderStatus
#
# Р­С‚Рѕ РґРѕРїСѓСЃС‚РёРјРѕ Рё РїРѕРґРґРµСЂР¶РёРІР°РµС‚СЃСЏ
OrderStatus = OrderStatus

