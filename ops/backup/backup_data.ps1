param(
    [string]$ProjectName = "job scraper",
    [string]$BackupRoot = "./ops/backup/artifacts"
)

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = Join-Path $BackupRoot $timestamp
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null

$xlsxFiles = Get-ChildItem -Path . -Filter "dotnet_jobs_*.xlsx" -File -ErrorAction SilentlyContinue
foreach ($file in $xlsxFiles) {
    Copy-Item -Path $file.FullName -Destination (Join-Path $backupDir $file.Name) -Force
}

$zipPath = Join-Path $BackupRoot ("backup_" + $timestamp + ".zip")
Compress-Archive -Path (Join-Path $backupDir "*") -DestinationPath $zipPath -Force

Write-Host "Backup created: $zipPath"
