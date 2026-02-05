param(
    [switch]$Soft
)

$ErrorActionPreference = "Stop"
$ROOT = "bot"
$CALLBACKS = "$ROOT/constants/callbacks.py"

$Errors = @()

# --- collect declared CallbackData classes
$Declared = @{}
Get-Content $CALLBACKS | ForEach-Object {
    if ($_ -match 'class\s+([A-Za-z0-9_]+)\s*\(\s*CallbackData') {
        $Declared[$matches[1]] = $true
    }
}

Get-ChildItem $ROOT -Recurse -Filter *.py | ForEach-Object {
    $File = $_.FullName
    $LineNo = 0

    Get-Content $File | ForEach-Object {
        $LineNo++
        $Line = $_

        # ❌ string callback_data
        if ($Line -match 'callback_data\s*=\s*".*"') {
            $Errors += ("{0}:{1} string callback_data запрещён" -f $File, $LineNo)
        }

        # ❌ callback_data=Class (без pack)
        if ($Line -match 'callback_data\s*=\s*([A-Za-z0-9_]+)\s*[,\)]') {
            $CB = $matches[1]
            if ($Declared.ContainsKey($CB)) {
                $Errors += ("{0}:{1} callback_data={2} без .pack()" -f $File, $LineNo, $CB)
            }
        }

        # ❌ legacy parsing
        if ($Line -match '\.split\(') {
            $Errors += ("{0}:{1} .split() запрещён" -f $File, $LineNo)
        }

        if ($Line -match 'startswith\(') {
            $Errors += ("{0}:{1} startswith() запрещён" -f $File, $LineNo)
        }
    }
}

if ($Errors.Count -gt 0) {
    Write-Host "`n❌ SUPER GUARD ERRORS:" -ForegroundColor Red
    $Errors | Sort-Object | ForEach-Object { Write-Host $_ -ForegroundColor Red }

    if (-not $Soft) {
        exit 1
    }
} else {
    Write-Host "✅ SUPER GUARD PASSED" -ForegroundColor Green
}

exit 1
