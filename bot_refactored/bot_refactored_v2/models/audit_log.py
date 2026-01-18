from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from bot_refactored.db import Base

class AuditLog(Base):
    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(primary_key=True)
    actor_id: Mapped[int | None]
    action: Mapped[str]
    entity: Mapped[str]
    entity_id: Mapped[int | None]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

