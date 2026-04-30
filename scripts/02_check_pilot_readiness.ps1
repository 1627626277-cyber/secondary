param(
    [string]$ProjectDir = "D:\二区",
    [int]$MinFreeGB = 300
)

$drive = [System.IO.DriveInfo]::new((Split-Path -Qualifier $ProjectDir) + "\")
$freeGB = [math]::Round($drive.AvailableFreeSpace / 1GB, 2)
$totalGB = [math]::Round($drive.TotalSize / 1GB, 2)

Write-Host "Project directory: $ProjectDir"
Write-Host "Drive total: $totalGB GiB"
Write-Host "Drive free : $freeGB GiB"
if ($freeGB -lt $MinFreeGB) {
    Write-Host "STATUS: STOP - free space is below $MinFreeGB GiB."
} else {
    Write-Host "STATUS: OK - enough space for one-sample pilot."
}

$requiredFiles = @(
    "GSE269875_family.soft.gz",
    "sample_manifest.tsv",
    "hg38.fa",
    "mm10.fa",
    "hg38.mmi",
    "mm10.mmi"
)

Write-Host ""
Write-Host "File readiness:"
foreach ($name in $requiredFiles) {
    $path = Join-Path $ProjectDir $name
    if (Test-Path -LiteralPath $path) {
        Write-Host "[OK]      $name"
    } else {
        Write-Host "[MISSING] $name"
    }
}

Write-Host ""
Write-Host "Tool readiness in current shell:"
$tools = @("prefetch", "fasterq-dump", "vdb-dump", "minimap2", "samtools")
foreach ($tool in $tools) {
    $cmd = Get-Command $tool -ErrorAction SilentlyContinue
    if ($cmd) {
        Write-Host "[OK]      $tool -> $($cmd.Source)"
    } else {
        Write-Host "[MISSING] $tool"
    }
}
