param(
    [Parameter(Mandatory = $true)]
    [string]$ArchivePath
)

if (-not (Test-Path $ArchivePath)) {
    throw "Archive not found: $ArchivePath"
}

$tempDir = Join-Path $env:TEMP ("job_scraper_restore_" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Force -Path $tempDir | Out-Null

Expand-Archive -Path $ArchivePath -DestinationPath $tempDir -Force

Get-ChildItem -Path $tempDir -Filter "dotnet_jobs_*.xlsx" -File -Recurse | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination (Join-Path (Get-Location) $_.Name) -Force
}

Remove-Item -Path $tempDir -Recurse -Force
Write-Host "Restore complete from: $ArchivePath"
