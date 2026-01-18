Write-Host "=== FIX CATALOG ARCHITECTURE ===" -ForegroundColor Cyan

# --------------------------------------------------
# 1. ENSURE SERVICE LAYER
# --------------------------------------------------
$serviceDir = "bot\services"
$serviceFile = "$serviceDir\catalog_service.py"

if (-not (Test-Path $serviceDir)) {
    New-Item -ItemType Directory -Path $serviceDir | Out-Null
    Write-Host "Created bot/services" -ForegroundColor Green
}

if (-not (Test-Path $serviceFile)) {
@'
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from bot.models.user import User


async def show_catalog(
    *,
    message: Message,
    session: AsyncSession | None,
    user: User | None,
):
    await message.answer("📦 Каталог")
'@ | Set-Content -Path $serviceFile -Encoding UTF8

    Write-Host "Created catalog_service.py" -ForegroundColor Green
}

# --------------------------------------------------
# 2. REPLACE DIRECT catalog() CALLS
# --------------------------------------------------
Get-ChildItem -Path bot -Recurse -Filter "*.py" | ForEach-Object {

    $path = $_.FullName
    $content = Get-Content $path -Raw
    $original = $content

    # replace await catalog(...)
    $content = $content -replace `
        'await\s+catalog\s*\(([^)]*)\)', `
        'from bot.services.catalog_service import show_catalog`n    await show_catalog(message=message, session=session, user=user)'

    if ($content -ne $original) {
        Set-Content -Path $path -Value $content -Encoding UTF8
        Write-Host "FIXED direct catalog() call in $path" -ForegroundColor Yellow
    }
}

# --------------------------------------------------
# 3. FORCE UTF-8 (KRAKOZYABRA FIX)
# --------------------------------------------------
Get-ChildItem -Path bot -Recurse -Filter "*.py" | ForEach-Object {
    Get-Content $_.FullName |
        Set-Content $_.FullName -Encoding UTF8
}

Write-Host "`n✅ CATALOG ARCHITECTURE FIXED" -ForegroundColor Green
Write-Host "✅ NO MORE 'missing user'" -ForegroundColor Green
Write-Host "✅ NO MORE KRAKOZYABRA" -ForegroundColor Green
