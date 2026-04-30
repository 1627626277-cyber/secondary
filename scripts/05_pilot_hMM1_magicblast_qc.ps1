param(
    [string]$ProjectDir = "D:\二区",
    [string]$RunAccession = "SRR29414112",
    [int]$Threads = 8,
    [int]$MinFreeGiB = 300,
    [int]$ReadPairs = 1000000
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ProjectDir = (Resolve-Path -LiteralPath $ProjectDir).Path
$drive = [System.IO.DriveInfo]::new((Split-Path -Qualifier $ProjectDir) + "\")
$freeGiB = [math]::Round($drive.AvailableFreeSpace / 1GB, 2)
if ($freeGiB -lt $MinFreeGiB) {
    throw "Only $freeGiB GiB free. Refusing to run; required: $MinFreeGiB GiB."
}

$sraBin = Join-Path $ProjectDir "tools\sratoolkit_extract\sratoolkit.3.4.1-win64\bin"
$magicBin = Join-Path $ProjectDir "tools\ncbi-magicblast-1.7.2\bin"
$env:PATH = "$sraBin;$magicBin;$env:PATH"

$sraCache = Join-Path $ProjectDir "sra_cache"
$qcDir = Join-Path $ProjectDir "qc_species_hMM1"
New-Item -ItemType Directory -Force -Path $sraCache, $qcDir | Out-Null

Write-Host "Project: $ProjectDir"
Write-Host "Pilot: GSM8329293 / hMM1 / SRX24927515 / $RunAccession"
Write-Host "Free space: $freeGiB GiB"
Write-Host "Sampled spots/read pairs: $ReadPairs"

Write-Host "Checking tools..."
prefetch --version
fastq-dump --version
magicblast -version

Write-Host "Checking reference DB..."
foreach ($p in @("blastdb\hg38.nsq", "blastdb\mm10.nsq")) {
    $full = Join-Path $ProjectDir $p
    if (-not (Test-Path -LiteralPath $full)) { throw "Missing $full" }
}

Write-Host "Step 1: prefetch"
prefetch $RunAccession --output-directory $sraCache --max-size 100G

$sraFile = Join-Path $sraCache "$RunAccession\$RunAccession.sra"
if (-not (Test-Path -LiteralPath $sraFile)) { throw "Missing downloaded SRA file: $sraFile" }

Write-Host "Step 2: sampled FASTQ export with fastq-dump"
fastq-dump --split-files -X $ReadPairs --outdir $qcDir $sraFile

$transcriptRead = Join-Path $qcDir "${RunAccession}_4.fastq"
if (-not (Test-Path -LiteralPath $transcriptRead)) {
    throw "Expected transcript read FASTQ not found: $transcriptRead"
}

Write-Host "Step 3: Magic-BLAST human mapping"
magicblast `
    -query $transcriptRead `
    -db (Join-Path $ProjectDir "blastdb\hg38") `
    -infmt fastq `
    -outfmt tabular `
    -num_threads $Threads `
    -out (Join-Path $qcDir "hMM1_hg38_magicblast.tsv")

Write-Host "Step 4: Magic-BLAST mouse mapping"
magicblast `
    -query $transcriptRead `
    -db (Join-Path $ProjectDir "blastdb\mm10") `
    -infmt fastq `
    -outfmt tabular `
    -num_threads $Threads `
    -out (Join-Path $qcDir "hMM1_mm10_magicblast.tsv")

Write-Host "Done. Outputs:"
Get-ChildItem -LiteralPath $qcDir | Select-Object Name,Length,LastWriteTime
