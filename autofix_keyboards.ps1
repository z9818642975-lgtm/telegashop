param(
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$ROOT = "bot\keyboards"
$BACKUP = "bot\.cb_backup"
$CALLBACKS_FILE = "bot\constants\callbacks.py"

Write-Host "== AUTOFIX KEYBOARDS =="

# --- backup
if (-not (Test-Path $BACKUP)) {
    New-Item -ItemType Directory -Path $BACKUP | Out-Null
}

# --- load existing CallbackData classes
$Declared = @{}
Get-Content $CALLBACKS_FILE | ForEach-Object {
    if ($_ -match 'class\s+([A-Za-z0-9_]+)\s*\(\s*CallbackData') {
        $Declared[$matches[1]] = $true
    }
}

# --- helper: string -> CB class name
function Get-CBName($value) {
    $clean = $value -replace '[^A-Za-z0-9]', '_'
    return ($clean.Substring(0,1).ToUpper() + $clean.Substring(1)) + "CB"
}

# --- scan keyboards
Get-ChildItem $ROOT -Recurse -Filter *.py | ForEach-Object {

    $File = $_.FullName
    $Rel  = $File.Replace("\", "/")

    $Lines = Get-Content $File
    $Changed = $false

    for ($i = 0; $i -lt $Lines.Count; $i++) {

        if ($Lines[$i] -match 'callback_data\s*=\s*"([^"]+)"') {

            $value = $matches[1]
            $cb = Get-CBName $value

            # --- register CB if missing
            if (-not $Declared.ContainsKey($cb)) {
@"
class $cb(CallbackData, prefix="$value"):
    pass

"@ | Add-Content $CALLBACKS_FILE

                $Declared[$cb] = $true
                Write-Host "  + CallbackData $cb"
            }

            # --- replace line
            $Lines[$i] = $Lines[$i] -replace 'callback_data\s*=\s*"[^"]+"', "callback_data=$cb().pack()"
            $Changed = $true
        }
    }

    if ($Changed) {
        $backupPath = Join-Path $BACKUP $Rel
        $backupDir = Split-Path $backupPath
        if (-not (Test-Path $backupDir)) {
            New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
        }

        Copy-Item $File $backupPath -Force

        if (-not $DryRun) {
            Set-Content $File $Lines -Encoding UTF8
        }

        Write-Host "✔ fixed $Rel"
    }
}

Write-Host "== AUTOFIX DONE =="
