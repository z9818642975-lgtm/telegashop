$ErrorActionPreference = "Stop"

Write-Host "🔍 Проверка wildcard handlers..."
Select-String -Path bot\routers\**\*.py -Pattern '@router\.message\(\s*\)' |
ForEach-Object {
    Write-Host "❌ WILDCARD:" $_.Path ":" $_.LineNumber
}

Write-Host "`n🔍 Проверка дубликатов F.text..."
$map = @{}
Select-String -Path bot\routers\operator\**\*.py -Pattern 'F\.text\s*==\s*"([^"]+)"' |
ForEach-Object {
    $text = $_.Matches[0].Groups[1].Value
    if ($map.ContainsKey($text)) {
        Write-Host "❌ DUPLICATE BUTTON: $text"
        Write-Host "   → $($map[$text])"
        Write-Host "   → $($_.Path):$($_.LineNumber)"
    } else {
        $map[$text] = "$($_.Path):$($_.LineNumber)"
    }
}

Write-Host "`n🔍 Проверка FSM конфликтов..."
Select-String -Path bot\**\*.py -Pattern 'StatesGroup' |
Group-Object Path |
Where-Object { $_.Count -gt 1 } |
ForEach-Object {
    Write-Host "⚠️ FSM POSSIBLE CONFLICT:" $_.Name
}

Write-Host "`n✅ Проверка завершена"
