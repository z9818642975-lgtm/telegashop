Write-Host "Removing __pycache__..."
Get-ChildItem . -Recurse -Directory -Filter "__pycache__" |
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "Removing .pyc..."
Get-ChildItem . -Recurse -File -Filter "*.pyc" |
    Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "✔ Python cache cleaned"
