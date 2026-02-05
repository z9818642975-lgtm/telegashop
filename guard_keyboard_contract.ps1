# guard_keyboard_contract.ps1
# Жёсткий guard: файл ↔ имя keyboard-функции

$ErrorActionPreference = "Continue"
$root = "bot/keyboards"
$errors = @()

Get-ChildItem $root -Recurse -Filter *.py | ForEach-Object {
    $file = $_.FullName
    $name = $_.BaseName

    if ($name -eq "__init__") { return }

    $expected = "${name}_kb"
    $content = Get-Content $file

    $found = $false
    foreach ($line in $content) {
        if ($line -match "def\s+$expected\s*\(") {
            $found = $true
            break
        }
    }

    if (-not $found) {
        $errors += "❌ $file → expected def $expected(...)"
    }

    foreach ($line in $content) {
        if ($line -match "_inline_kb") {
            $errors += "❌ $file → legacy *_inline_kb запрещён"
        }
    }
}

if ($errors.Count -gt 0) {
    Write-Host "`nKEYBOARD CONTRACT VIOLATIONS:" -ForegroundColor Red
    $errors | ForEach-Object { Write-Host $_ -ForegroundColor Red }
    Write-Host "`n⛔ Guard failed"
} else {
    Write-Host "✅ Keyboard contract OK" -ForegroundColor Green
}
