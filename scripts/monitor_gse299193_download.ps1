param(
    [int]$IntervalSeconds = 120
)

$ErrorActionPreference = "Continue"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Project = Resolve-Path (Join-Path $ScriptDir "..")
$ExpectedBytes = 82255360000
$RawTar = Join-Path $Project "external_spatial\GSE299193\raw\GSE299193_RAW.tar"
$StartScript = Join-Path $Project "scripts\start_gse299193_download.ps1"
$StatusScript = Join-Path $Project "scripts\17_gse299193_download_status.py"
$MonitorLog = Join-Path $Project "run_logs\gse299193_monitor.log"
$Heartbeat = Join-Path $Project "reports\validation\GSE299193_DOWNLOAD_WATCHDOG.md"

New-Item -ItemType Directory -Force -Path (Split-Path -Parent $MonitorLog), (Split-Path -Parent $Heartbeat), (Split-Path -Parent $RawTar) | Out-Null

function Write-MonitorLog {
    param([string]$Message)
    $line = "[{0}] {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $Message
    Add-Content -Path $MonitorLog -Value $line -Encoding UTF8
}

function Get-RawTarSize {
    if (Test-Path $RawTar) {
        return (Get-Item $RawTar).Length
    }
    return 0
}

function Get-GseCurlProcess {
    Get-CimInstance Win32_Process -Filter "Name = 'curl.exe'" |
        Where-Object { $_.CommandLine -like "*GSE299193_RAW.tar*" }
}

function Write-Heartbeat {
    param(
        [long]$SizeBytes,
        [object[]]$Processes,
        [string]$State
    )

    $remaining = [Math]::Max($ExpectedBytes - $SizeBytes, 0)
    $pct = if ($ExpectedBytes -gt 0) { ($SizeBytes / $ExpectedBytes) * 100 } else { 0 }
    $now = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $sizeGib = [Math]::Round($SizeBytes / 1GB, 3)
    $pctRounded = [Math]::Round($pct, 4)
    $remainingGib = [Math]::Round($remaining / 1GB, 3)
    $expectedGib = [Math]::Round($ExpectedBytes / 1GB, 3)
    $processText = if ($Processes -and $Processes.Count -gt 0) {
        $processLines = foreach ($proc in $Processes) {
            "- PID {0} command: {1}" -f $proc.ProcessId, $proc.CommandLine
        }
        $processLines -join [Environment]::NewLine
    } else {
        "- No active GSE299193 curl process detected."
    }

    $lines = @(
        "# GSE299193 Download Watchdog",
        "",
        ("- Last check: {0}." -f $now),
        ("- State: {0}." -f $State),
        ("- Current size: {0} bytes / {1} GiB." -f $SizeBytes, $sizeGib),
        ("- Percent complete: {0}%." -f $pctRounded),
        ("- Remaining: {0} GiB." -f $remainingGib),
        ("- Expected size: {0} bytes / {1} GiB." -f $ExpectedBytes, $expectedGib),
        "",
        "Active process:",
        "",
        $processText,
        "",
        "Logs:",
        "",
        "- Monitor log: run_logs\gse299193_monitor.log.",
        "- Download stderr: run_logs\gse299193_download_stderr.log.",
        "- Status report: reports\validation\GSE299193_XENIUM_DOWNLOAD_STATUS.md.",
        ""
    )
    Set-Content -Path $Heartbeat -Value ($lines -join "`n") -Encoding UTF8
}

Write-MonitorLog "Watchdog started. interval_seconds=$IntervalSeconds"

while ($true) {
    try {
        $size = Get-RawTarSize
        $processes = @(Get-GseCurlProcess)

        if ($size -ge $ExpectedBytes) {
            Write-MonitorLog "Download appears complete. size_bytes=$size"
            Write-Heartbeat -SizeBytes $size -Processes $processes -State "complete"
            if (Test-Path $StatusScript) {
                & python $StatusScript *> (Join-Path $Project "run_logs\gse299193_status_refresh.log")
            }
            break
        }

        if (-not $processes -or $processes.Count -eq 0) {
            Write-MonitorLog "No active curl process; restarting resumable download. size_bytes=$size"
            $restartArgs = @(
                "-NoProfile",
                "-ExecutionPolicy", "Bypass",
                "-File", $StartScript
            )
            $restartProcess = Start-Process -FilePath "powershell.exe" -ArgumentList $restartArgs -WindowStyle Hidden -PassThru
            Write-MonitorLog "Started resumable download launcher. launcher_pid=$($restartProcess.Id)"
            Start-Sleep -Seconds 20
            $processes = @(Get-GseCurlProcess)
        }

        Write-Heartbeat -SizeBytes (Get-RawTarSize) -Processes $processes -State "downloading"

        if (Test-Path $StatusScript) {
            & python $StatusScript *> (Join-Path $Project "run_logs\gse299193_status_refresh.log")
        }
    } catch {
        Write-MonitorLog "Watchdog error: $($_.Exception.Message)"
        Write-Heartbeat -SizeBytes (Get-RawTarSize) -Processes @(Get-GseCurlProcess) -State "watchdog_error"
    }

    Start-Sleep -Seconds $IntervalSeconds
}

Write-MonitorLog "Watchdog stopped."
