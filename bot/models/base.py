from __future__ import annotations

from typing import TYPE_CHECKING

# bot/models/base.py
from sqlalchemy.orm import DeclarativeBase

if TYPE_CHECKING:
    pass


class Base(DeclarativeBase):
    pass

# noqa: F821
