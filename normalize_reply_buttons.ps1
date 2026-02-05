# bot/tools/normalize_reply_buttons.py
$ErrorActionPreference = "Stop"

# -----------------------------
# НАСТРОЙКИ
# -----------------------------
$adminPrefix = "А "
$operatorPrefix = "О "

$adminPaths = @(
    "bot\keyboards\admin",
    "bot\routers\admin"
)

$operatorPaths = @(
    "bot\keyboards\operator",
    "bot\routers\operator"
)

# -----------------------------
# ФУНКЦИЯ ОБРАБОТКИ
# -----------------------------
function Normalize-Files($paths, $prefix) {
    foreach ($path in $paths) {
        Get-ChildItem -Path $path -Recurse -Filter *.py | ForEach-Object {
            $file = $_.FullName
            $content = Get-Content $file -Raw

            $original = $content

            # text="..."
            $content = $content -replace 'text="([^"]+)"', {
                param($m)
                $text = $m.Groups[1].Value
                if ($text.StartsWith($prefix)) { return $m.Value }
                return 'text="' + $prefix + $text + '"'
            }

            # F.text == "..."
            $content = $content -replace 'F\.text\s*==\s*"([^"]+)"', {
                param($m)
                $text = $m.Groups[1].Value
                if ($text.StartsWith($prefix)) { return $m.Value }
                return 'F.text == "' + $prefix + $text + '"'
            }

            if ($content -ne $original) {
                Set-Content -Path $file -Value $content -Encoding UTF8
                Write-Host "✏ $file"
            }
        }
    }
}

# -----------------------------
# ЗАПУСК
# -----------------------------
Normalize-Files $adminPaths $adminPrefix
Normalize-Files $operatorPaths $operatorPrefix

Write-Host "`n✅ Готово. Кнопки нормализованы по ролям."
