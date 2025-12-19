# bot/core/config.py
from __future__ import annotations

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    # ✅ ТОЛЬКО pydantic v2 стиль
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow",        # разрешаем лишние env (LOKI, WATCHDOG и т.д.)
        case_sensitive=True,
    )

    BOT_TOKEN: str
    DATABASE_URL: str
    REDIS_URL: str = "redis://redis:6379/0"
    ADMINS: List[int] = []
    HEALTH_PORT: int = 8080
    TZ: str = "Europe/Oslo"

    @field_validator("ADMINS", mode="before")
    @classmethod
    def parse_admins(cls, v):
        if isinstance(v, list):
            return v
        if not v:
            return []
        return [int(x.strip()) for x in str(v).split(",") if x.strip()]


settings = Settings()
