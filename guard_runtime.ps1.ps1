param([switch]$Soft)

$ErrorActionPreference = "Continue"

$ROOT = "bot"
$EXCLUDE = @(
    "\.cb_backup\",
    "\config.py",
    "\bootstrap\",
    "\services\",
    "\db\",
    "\models\",
    "\utils\",
    "\tools\"
)

$Errors = @()

Get-ChildItem $ROOT -Recurse -Filter *.py | ForEach-Object {
    $file = $_.FullName

    foreach ($e in $EXCLUDE) {
        if ($file -match [regex]::Escape($e)) { return }
    }

    $i = 0
    Get-Content $file | ForEach-Object {
        $i++
        $line = $_

        if ($line -match 'callback_data\s*=\s*".*"') {
            $Errors += "$file:$i string callback_data запрещён"
        }

        if (
            $line -match 'cb\.data' -and
            ($line -match '\.split\(' -or $line -match 'startswith\(')
        ) {
            $Errors += "$file:$i legacy cb.data parsing"
        }
    }
}

if ($Errors.Count -gt 0) {
    Write-Host "`n❌ RUNTIME CALLBACK ERRORS:" -ForegroundColor Red
    $Errors | ForEach-Object { Write-Host $_ -ForegroundColor Red }
    if (-not $Soft) { exit 1 }
} else {
    Write-Host "✅ Runtime callback guard passed" -ForegroundColor Green
}
