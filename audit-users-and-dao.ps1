Write-Host "=== AUDIT START ==="

$patterns = @(
    "username",
    "full_name",
    "DAO\.",
    "get_or_create\(",
    "get_or_create_by_tg_id",
    "UsersDAO\.",
    "ProductsDAO\.",
    "OrdersDAO\."
)

foreach ($p in $patterns) {
    Write-Host "`n--- Pattern: $p ---"
    Get-ChildItem .\bot -Recurse -File |
        Select-String -Pattern $p |
        Select-Object Path, LineNumber, Line
}

Write-Host "`n=== AUDIT END ==="
