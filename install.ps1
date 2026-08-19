# ==============================================================================
# SEO Skills AI — Isolated Runtime Installer (Windows PowerShell)
# ==============================================================================
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$InstallDir = Join-Path $env:USERPROFILE ".config\seoskillsai"
$VenvDir = Join-Path $InstallDir "venv"
$PythonExe = Join-Path $VenvDir "Scripts\python.exe"

Write-Host "==> [SEO Skills AI] Initializing isolated runtime for Windows..." -ForegroundColor Cyan

if (-not (Test-Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
}

# Locate system python
$SysPython = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $SysPython) {
    $SysPython = (Get-Command py -ErrorAction SilentlyContinue).Source
}

if (-not $SysPython) {
    Write-Error "Python 3.10+ is required but not found on PATH. Please install Python from https://python.org"
    exit 1
}

Write-Host "==> [SEO Skills AI] Found Python: $SysPython" -ForegroundColor Green

# Create isolated venv
if (-not (Test-Path $PythonExe)) {
    Write-Host "==> [SEO Skills AI] Creating isolated virtualenv in $VenvDir..." -ForegroundColor Yellow
    & $SysPython -m venv $VenvDir
}

# Upgrade pip & install dependencies
Write-Host "==> [SEO Skills AI] Installing core Python dependencies..." -ForegroundColor Yellow
& $PythonExe -m pip install --quiet --upgrade pip setuptools wheel
& $PythonExe -m pip install --quiet requests beautifulsoup4 urllib3 pytest playwright

Write-Host "==> [SEO Skills AI] Installing Playwright Chromium browser..." -ForegroundColor Yellow
try {
    & $PythonExe -m playwright install chromium
} catch {
    Write-Host "Playwright browser setup skipped or already completed." -ForegroundColor Gray
}

Write-Host "==> [SEO Skills AI] Windows runtime setup complete!" -ForegroundColor Green
Write-Host "    You can now run /seo audit <url> in your AI assistant." -ForegroundColor Cyan
