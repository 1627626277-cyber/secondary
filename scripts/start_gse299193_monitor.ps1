$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Project = Resolve-Path (Join-Path $ScriptDir "..")
$MonitorScript = Join-Path $Project "scripts\monitor_gse299193_download.ps1"
$Stdout = Join-Path $Project "run_logs\gse299193_monitor_stdout.log"
$Stderr = Join-Path $Project "run_logs\gse299193_monitor_stderr.log"

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Stdout) | Out-Null

$existing = Get-CimInstance Win32_Process -Filter "Name = 'powershell.exe'" |
    Where-Object { $_.CommandLine -like "*monitor_gse299193_download.ps1*" }

if ($existing) {
    [PSCustomObject]@{
        Status = "already_running"
        ProcessId = ($existing | Select-Object -First 1).ProcessId
        MonitorScript = $MonitorScript
    }
    exit 0
}

$arguments = @(
    "-NoProfile",
    "-ExecutionPolicy", "Bypass",
    "-File", $MonitorScript,
    "-IntervalSeconds", "120"
)

$process = Start-Process -FilePath "powershell.exe" `
    -ArgumentList $arguments `
    -RedirectStandardOutput $Stdout `
    -RedirectStandardError $Stderr `
    -WindowStyle Hidden `
    -PassThru

[PSCustomObject]@{
    Status = "started"
    ProcessId = $process.Id
    MonitorScript = $MonitorScript
    StdoutLog = $Stdout
    StderrLog = $Stderr
}
