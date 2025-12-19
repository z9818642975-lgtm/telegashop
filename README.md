# TelegaShop — FINAL PROD FULL

## Запуск (Docker)
```bash
cp .env.example .env
# edit .env (BOT_TOKEN)
docker compose up -d --build
docker compose exec bot alembic upgrade head
```
Health:
- http://localhost:8080/health

## Оператор
- /op
- /shift_start <адрес>
- /shift_end
