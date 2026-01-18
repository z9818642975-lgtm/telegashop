#!/bin/bash
set -e

echo "🧩 Waiting for PostgreSQL (asyncpg)..."

python - << 'EOF'
import asyncio
import os
import asyncpg

raw_dsn = os.getenv("DATABASE_URL")
if not raw_dsn:
    raise RuntimeError("DATABASE_URL is not set")

# asyncpg НЕ принимает postgresql+asyncpg://
dsn = raw_dsn.replace("postgresql+asyncpg://", "postgresql://")

async def wait_db():
    while True:
        try:
            conn = await asyncpg.connect(dsn)
            await conn.close()
            print("🧩 PostgreSQL is ready")
            return
        except Exception as e:
            print("⏳ Waiting for PostgreSQL...", e)
            await asyncio.sleep(2)

asyncio.run(wait_db())
EOF

#echo "🧩 Applying migrations (upgrade heads)..."
#Salembic upgrade heads

echo "🧩 Starting bot..."
exec python -m bot.main
