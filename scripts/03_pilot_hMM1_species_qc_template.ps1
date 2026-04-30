param(
    [string]$ProjectDir = "D:\二区",
    [string]$PilotAccession = "SRX24927515",
    [int]$Threads = 8,
    [int]$DiskLimitGB = 300
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$drive = [System.IO.DriveInfo]::new((Split-Path -Qualifier $ProjectDir) + "\")
$freeGB = [math]::Round($drive.AvailableFreeSpace / 1GB, 2)
if ($freeGB -lt $DiskLimitGB) {
    throw "Only $freeGB GiB free. Refusing to run because the pilot requires at least $DiskLimitGB GiB."
}

$sraCache = Join-Path $ProjectDir "sra_cache"
$fastqDir = Join-Path $ProjectDir "fastq"
$tmpDir = Join-Path $ProjectDir "tmp_fasterq"
$qcDir = Join-Path $ProjectDir "qc_species_hMM1"
New-Item -ItemType Directory -Force -Path $sraCache, $fastqDir, $tmpDir, $qcDir | Out-Null

Write-Host "Pilot sample: GSM8329293 / hMM1"
Write-Host "Pilot accession: $PilotAccession"
Write-Host "Free space: $freeGB GiB"

Write-Host ""
Write-Host "Step 1: prefetch"
prefetch $PilotAccession --output-directory $sraCache --max-size 100G

Write-Host ""
Write-Host "Step 2: size check only"
fasterq-dump $PilotAccession `
    --outdir $fastqDir `
    --temp $tmpDir `
    --threads $Threads `
    --size-check only `
    --disk-limit "${DiskLimitGB}GB"

Write-Host ""
Write-Host "Step 3: FASTQ conversion"
fasterq-dump $PilotAccession `
    --split-files `
    --outdir $fastqDir `
    --temp $tmpDir `
    --threads $Threads `
    --progress `
    --disk-limit "${DiskLimitGB}GB"

Write-Host ""
Write-Host "Step 4: find FASTQ outputs"
$r1 = Get-ChildItem -LiteralPath $fastqDir -Filter "*_1.fastq" | Sort-Object Length -Descending | Select-Object -First 1
$r2 = Get-ChildItem -LiteralPath $fastqDir -Filter "*_2.fastq" | Sort-Object Length -Descending | Select-Object -First 1
if (-not $r1 -or -not $r2) {
    throw "Could not find paired FASTQ outputs in $fastqDir"
}
Write-Host "R1: $($r1.FullName)"
Write-Host "R2: $($r2.FullName)"

Write-Host ""
Write-Host "Step 5: human/mouse mapping QC"
$hg38 = Join-Path $ProjectDir "hg38.mmi"
$mm10 = Join-Path $ProjectDir "mm10.mmi"
if (-not (Test-Path -LiteralPath $hg38)) { throw "Missing hg38 index: $hg38" }
if (-not (Test-Path -LiteralPath $mm10)) { throw "Missing mm10 index: $mm10" }

minimap2 -ax sr -t $Threads $hg38 $r1.FullName $r2.FullName | samtools flagstat - > (Join-Path $qcDir "hMM1_hg38_flagstat.txt")
minimap2 -ax sr -t $Threads $mm10 $r1.FullName $r2.FullName | samtools flagstat - > (Join-Path $qcDir "hMM1_mm10_flagstat.txt")

Write-Host ""
Write-Host "Done. Review:"
Write-Host (Join-Path $qcDir "hMM1_hg38_flagstat.txt")
Write-Host (Join-Path $qcDir "hMM1_mm10_flagstat.txt")
