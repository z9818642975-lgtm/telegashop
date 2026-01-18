# bot/config.py
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # === Telegram ===
    BOT_TOKEN: str = Field(..., env="BOT_TOKEN")

    # === Roles (RAW from env) ===
    ADMIN_ID: int | None = Field(default=None, env="ADMIN_ID")
    ADMINS_RAW: str = Field(default="", env="ADMINS")
    OPERATORS_RAW: str = Field(default="", env="OPERATORS")

    # === Infrastructure (RAW) ===
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    REDIS_URL: str = Field(..., env="REDIS_URL")

    # === Optional / infra flags ===
    ENVIRONMENT: str | None = None
    TIMEZONE: str | None = None
    LOKI_MODE: bool | None = None
    LOKI_URL: str | None = None
    WATCHDOG_ENABLED: bool | None = None
    WATCHDOG_INTERVAL_SECONDS: int | None = None

    # === Pydantic v2 config ===
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ============================================================
    # PARSED / NORMALIZED PROPERTIES
    # ============================================================

    @property
    def database_url(self) -> str:
        return self.DATABASE_URL

    @property
    def redis_url(self) -> str:
        return self.REDIS_URL

    @property
    def ADMINS(self) -> set[int]:
        return {
            int(x.strip())
            for x in self.ADMINS_RAW.split(",")
            if x.strip()
        }

    @property
    def OPERATORS(self) -> set[int]:
        return {
            int(x.strip())
            for x in self.OPERATORS_RAW.split(",")
            if x.strip()
        }


settings = Settings()
