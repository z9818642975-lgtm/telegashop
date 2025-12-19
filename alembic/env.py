# alembic/env.py
from __future__ import annotations

import sys
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

# ------------------------------------------------------------
# PYTHONPATH FIX
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# ------------------------------------------------------------
from bot.core.config import settings
from bot.core.db import Base

# ------------------------------------------------------------
# Alembic Config
# ------------------------------------------------------------
config = context.config
target_metadata = Base.metadata


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def get_sync_database_url() -> str:
    """
    Alembic MUST use sync driver.
    """
    url = settings.DATABASE_URL
    if url.startswith("postgresql+asyncpg://"):
        return url.replace("postgresql+asyncpg://", "postgresql+psycopg://")
    return url


# ------------------------------------------------------------
# Offline migrations
# ------------------------------------------------------------
def run_migrations_offline() -> None:
    context.configure(
        url=get_sync_database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ------------------------------------------------------------
# Online migrations
# ------------------------------------------------------------
def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = get_sync_database_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# ------------------------------------------------------------
# Entrypoint
# ------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
