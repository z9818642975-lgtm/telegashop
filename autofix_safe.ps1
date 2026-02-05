$ErrorActionPreference = 'Stop'

$ProjectRoot = Get-Location
$KeyboardRoot = Join-Path $ProjectRoot 'bot\keyboards'
$BackupRoot   = Join-Path $ProjectRoot '.cb_backup'

Write-Host '== AUTOFIX SAFE =='

if (-not (Test-Path $BackupRoot)) {
    New-Item -ItemType Directory -Path $BackupRoot | Out-Null
}

Get-ChildItem -Path $KeyboardRoot -Recurse -Filter '*.py' | ForEach-Object {

    $File = $_.FullName
    $SafeName = ($File -replace '[\\/:*?"<>|]', '_')
    Copy-Item -LiteralPath $File -Destination (Join-Path $BackupRoot $SafeName) -Force

    $Input  = Get-Content -LiteralPath $File
    $Output = New-Object System.Collections.Generic.List[string]

    foreach ($Line in $Input) {
        if ($Line -match 'callback_data\s*=\s*"([^"]+)"') {
            $Key = $matches[1].ToUpper()
            $Output.Add(($Line -replace 'callback_data\s*=\s*".*?"', "callback_data=CB.$Key"))
        }
        else {
            $Output.Add($Line)
        }
    }

    Set-Content -LiteralPath $File -Value $Output -Encoding UTF8
}

Write-Host 'AUTOFIX DONE'
