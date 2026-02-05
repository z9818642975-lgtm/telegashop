$ErrorActionPreference = "Stop"

$root = "bot"
$bad = @()

$exclude = @(
    "bot\config.py",
    "bot\bootstrap\init_db.py"
)

Write-Host "== CB & CALLBACK GUARD =="

Get-ChildItem $root -Recurse -Filter *.py | ForEach-Object {
    $file = $_.FullName

    foreach ($e in $exclude) {
        if ($file.EndsWith($e)) { return }
    }

    $lines = Get-Content $file
    $i = 0

    foreach ($line in $lines) {
        $i++

        if (
            # f-string callback_data
            $line -match 'callback_data\s*=\s*f["'']' -or

            # legacy CB container
            $line -match '\bCB\.' -or

            # legacy parsing ONLY callback_data
            (
                $line -match 'cb\.data' -and
                (
                    $line -match '\.split\(' -or
                    $line -match 'startswith\('
                )
            )
        ) {
            $bad += "${file}:${i} -> ${line}"
        }
    }
}

if ($bad.Count -gt 0) {
    Write-Host ""
    Write-Host "CRITICAL CALLBACK ERRORS FOUND:" -ForegroundColor Red
    $bad | ForEach-Object { Write-Host $_ -ForegroundColor Red }
    exit 1
}

Write-Host "OK - callback layer clean"
