$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Project = Resolve-Path (Join-Path $ScriptDir "..")
$Url = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE299nnn/GSE299193/suppl/GSE299193_RAW.tar"
$Out = Join-Path $Project "external_spatial\GSE299193\raw\GSE299193_RAW.tar"
$Stdout = Join-Path $Project "run_logs\gse299193_download_stdout.log"
$Stderr = Join-Path $Project "run_logs\gse299193_download_stderr.log"

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Out), (Split-Path -Parent $Stdout) | Out-Null

$Arguments = @(
    "--location",
    "--ssl-no-revoke",
    "--ipv4",
    "--continue-at", "-",
    "--retry", "30",
    "--retry-all-errors",
    "--retry-delay", "30",
    "--connect-timeout", "60",
    "--speed-time", "300",
    "--speed-limit", "102400",
    "--output", $Out,
    $Url
)

$Process = Start-Process -FilePath "curl.exe" `
    -ArgumentList $Arguments `
    -RedirectStandardOutput $Stdout `
    -RedirectStandardError $Stderr `
    -WindowStyle Hidden `
    -PassThru

[PSCustomObject]@{
    ProcessId = $Process.Id
    OutputFile = $Out
    StdoutLog = $Stdout
    StderrLog = $Stderr
    Url = $Url
}
