$rules = @{
    "ProductsDAO.get_active\(([^)]*)\)" = "ProductsDAO(`$1).get_active()"
    "ProductsDAO.get_by_id\(([^,]+),\s*([^)]+)\)" = "ProductsDAO(`$1).get_by_id(`$2)"
    "OrdersDAO.get_active\(([^)]*)\)" = "OrdersDAO(`$1).get_active()"
}

Get-ChildItem .\bot -Recurse -File -Filter *.py | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $original = $content

    foreach ($rule in $rules.GetEnumerator()) {
        $content = $content -replace $rule.Key, $rule.Value
    }

    if ($content -ne $original) {
        Write-Host "Fixed:" $_.FullName
        Set-Content $_.FullName $content -Encoding UTF8
    }
}
