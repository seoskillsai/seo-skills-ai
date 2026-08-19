# SEO Skills AI — Windows Uninstaller
Write-Host "==> [SEO Skills AI] Uninstalling runtime and local configurations..." -ForegroundColor Cyan

$ConfigDir = Join-Path $HOME ".config\seoskillsai"
if (Test-Path $ConfigDir) {
    Remove-Item -Recurse -Force $ConfigDir
    Write-Host "  ✔ Removed configuration directory: $ConfigDir" -ForegroundColor Green
}

Write-Host "✔ [SEO Skills AI] Uninstallation completed cleanly." -ForegroundColor Green
