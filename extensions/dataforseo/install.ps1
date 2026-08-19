$ConfigDir = Join-Path $HOME ".config\seoskillsai"
if (-not (Test-Path $ConfigDir)) { New-Item -ItemType Directory -Path $ConfigDir -Force | Out-Null }
Write-Host "[SUCCESS] DataForSEO Extension initialized for Windows." -ForegroundColor Green
