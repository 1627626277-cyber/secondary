@echo off
setlocal

set "SRC_ROOT=C:\Users\jz\Documents\Codex\2026-04-28\files-mentioned-by-the-user-deep\tools"
set "DST_ROOT=D:\二区\tools"

echo Copying Windows-native toolchain to %DST_ROOT%
echo.

if not exist "D:\二区" (
  echo ERROR: D:\二区 does not exist.
  exit /b 1
)

mkdir "%DST_ROOT%" 2>nul

robocopy "%SRC_ROOT%\sratoolkit_extract\sratoolkit.3.4.1-win64" "%DST_ROOT%\sratoolkit.3.4.1-win64" /E
robocopy "%SRC_ROOT%\ncbi-magicblast-1.7.2" "%DST_ROOT%\ncbi-magicblast-1.7.2" /E

echo.
echo Add these tools to PATH in a new terminal with:
echo set PATH=D:\二区\tools\sratoolkit.3.4.1-win64\bin;D:\二区\tools\ncbi-magicblast-1.7.2\bin;%%PATH%%
echo.
echo Then verify:
echo prefetch --version
echo fasterq-dump --version
echo vdb-dump --version
echo magicblast -version
echo makeblastdb -version

endlocal
