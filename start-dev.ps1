param(
    [int]$BackendPort = 5000,
    [int]$FrontendPort = 5173
)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$frontendDir = Join-Path $projectRoot 'frontend'

if (-not (Test-Path (Join-Path $projectRoot 'api_server.py'))) {
    throw "api_server.py not found in project root: $projectRoot"
}

if (-not (Test-Path $frontendDir)) {
    throw "frontend directory not found: $frontendDir"
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "python is not available in PATH"
}

if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    throw "npm is not available in PATH"
}

$backendCmd = "Set-Location '$projectRoot'; python api_server.py"
$frontendCmd = "Set-Location '$frontendDir'; npm run dev"

Write-Host "Starting backend on port $BackendPort..."
Start-Process powershell -ArgumentList '-NoExit', '-Command', $backendCmd -WindowStyle Normal | Out-Null

Start-Sleep -Seconds 1

Write-Host "Starting frontend on port $FrontendPort..."
Start-Process powershell -ArgumentList '-NoExit', '-Command', $frontendCmd -WindowStyle Normal | Out-Null

Write-Host "Startup commands launched."
Write-Host "Frontend: http://localhost:$FrontendPort"
Write-Host "Backend:  http://127.0.0.1:$BackendPort"
