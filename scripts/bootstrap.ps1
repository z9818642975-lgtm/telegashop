Write-Host "Applying migrations..."
alembic upgrade head
Write-Host "Starting bot..."
python -m bot.main
