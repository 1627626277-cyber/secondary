@echo off
set "CODEX_TOOL_ROOT=C:\Users\jz\Documents\Codex\2026-04-28\files-mentioned-by-the-user-deep\tools"
set "PATH=%CODEX_TOOL_ROOT%\sratoolkit_extract\sratoolkit.3.4.1-win64\bin;%CODEX_TOOL_ROOT%\ncbi-magicblast-1.7.2\bin;%PATH%"
echo Windows-native bioinformatics toolchain is now on PATH for this terminal.
echo.
prefetch --version
fasterq-dump --version
vdb-dump --version
magicblast -version
makeblastdb -version
