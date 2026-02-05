param(
    [switch]$Soft
)

$ErrorActionPreference = 'Stop'

$ProjectRoot = Get-Location
$Root        = Join-Path $ProjectRoot 'bot'
$Callbacks   = Join-Path $Root 'constants\callbacks.py'

$Exclude = @(
    '.cb_backup',
    '__pycache__',
    '.git',
    '.venv'
)

$Errors   = New-Object System.Collections.Generic.List[string]
$Declared = @{}

Write-Host '== SUPER GUARD =='

# collect declared CallbackData classes
if (Test-Path $Callbacks) {
    Get-Content -LiteralPath $Callbacks | ForEach-Object {
        if ($_ -match 'class\s+([A-Za-z0-9_]+)\s*\(\s*CallbackData') {
            $Declared[$matches[1]] = $true
        }
    }
}

# scan python files
Get-ChildItem -Path $Root -Recurse -Filter '*.py' | ForEach-Object {

    $File = $_.FullName
    foreach ($e in $Exclude) {
        if ($File -like "*$e*") { return }
    }

    $LineNo = 0

    Get-Content -LiteralPath $File | ForEach-Object {
        $LineNo++
        $Line = $_

        if ($Line -match 'callback_data\s*=\s*".*"') {
            $Errors.Add(("{0}:{1} string callback_data forbidden" -f $File, $LineNo))
        }

        if ($Line -match 'callback_data\s*=\s*([A-Za-z0-9_]+)\s*[,\)]') {
            $cb = $matches[1]
            if ($Declared.ContainsKey($cb)) {
                $Errors.Add(("{0}:{1} callback_data={2} without .pack()" -f $File, $LineNo, $cb))
            }
        }

        if ($Line -match '\.split\(') {
            $Errors.Add(("{0}:{1} .split() forbidden" -f $File, $LineNo))
        }

        if ($Line -match 'startswith\(') {
            $Errors.Add(("{0}:{1} startswith() forbidden" -f $File, $LineNo))
        }
    }
}

if ($Errors.Count -gt 0) {
    Write-Host ''
    Write-Host 'SUPER GUARD ERRORS' -ForegroundColor Red
    $Errors | Sort-Object | ForEach-Object {
        Write-Host $_ -ForegroundColor Red
    }
    if (-not $Soft) {
        exit 1
    }
}
else {
    Write-Host 'OK - contract clean' -ForegroundColor Green
}
