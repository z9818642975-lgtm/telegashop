$ErrorActionPreference = "Stop"

$root = "bot"
$middleware = "DBSessionMiddleware"
$importLine = "from bot.db import async_session_maker"

Write-Host "== DBSessionMiddleware RESCUE v2 ==" -ForegroundColor Cyan

Get-ChildItem $root -Recurse -Filter *.py |
Where-Object { $_.FullName -notmatch '\\.cb_backup\\' } |
ForEach-Object {

    $file = $_
    $content = Get-Content $file.FullName -Raw
    $changed = $false

    if ($content -match "$middleware\(\)") {
        $content = $content -replace "$middleware\(\)", "$middleware(async_session_maker)"
        $changed = $true
    }

    if ($changed -and $content -notmatch "async_session_maker") {
        if ($content -match "(from .+\n)+") {
            $content = $content -replace "(from .+\n)+", "`$0$importLine`n"
        } elseif ($content -match "(import .+\n)+") {
            $content = $content -replace "(import .+\n)+", "`$0$importLine`n"
        } else {
            $content = "$importLine`n`n$content"
        }
    }

    if ($changed) {
        Set-Content $file.FullName $content -Encoding UTF8
        Write-Host "FIXED: $($file.FullName)" -ForegroundColor Green
    }
}

Write-Host "== DONE ==" -ForegroundColor Cyan
