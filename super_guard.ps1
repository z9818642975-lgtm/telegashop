$ROOT = "bot"
$CALLBACKS = "$ROOT/constants/callbacks.py"

$Declared = @{}
$Used = @{}
$Violations = @()

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

        if ($Line -match '\b([A-Za-z0-9_]+)\.filter\(') {
            $Used[$matches[1]] = $true
        }

        if ($Line -match '\.split\(') {
            $Violations += ("{0}:{1} legacy split()" -f $File, $LineNo)
        }

        if ($Line -match 'callback_data\s*=\s*".*"') {
            $Violations += ("{0}:{1} string callback_data" -f $File, $LineNo)
        }
    }
}

$Missing = $Used.Keys | Where-Object { -not $Declared.ContainsKey($_) }
$Orphan  = $Declared.Keys | Where-Object { -not $Used.ContainsKey($_) }

Write-Host "=== AUDIT REPORT ===" -ForegroundColor Cyan
Write-Host ("Declared: {0}" -f $Declared.Count)
Write-Host ("Used:     {0}" -f $Used.Count)

if ($Missing.Count -gt 0) {
    Write-Host "`n❌ Missing CallbackData:" -ForegroundColor Red
    $Missing | Sort-Object | ForEach-Object { Write-Host $_ -ForegroundColor Red }
}

if ($Orphan.Count -gt 0) {
    Write-Host "`n⚠ Orphan CallbackData:" -ForegroundColor Yellow
    $Orphan | Sort-Object | ForEach-Object { Write-Host $_ -ForegroundColor Yellow }
}

if ($Violations.Count -gt 0) {
    Write-Host "`n❌ Violations:" -ForegroundColor Red
    $Violations | Sort-Object | ForEach-Object { Write-Host $_ -ForegroundColor Red }
} else {
    Write-Host "`n✅ No violations found" -ForegroundColor Green
}
