# guard_ci.ps1
powershell -ExecutionPolicy Bypass -File super_guard.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "⛔ CI BLOCKED BY SUPER GUARD" -ForegroundColor Red
    exit 1
}
Write-Host "✅ CI PASSED" -ForegroundColor Green
exit 1
