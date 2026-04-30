@echo off
set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..") do set "PROJECT_ROOT=%%~fI"
set "PATH=%PROJECT_ROOT%\tools\sratoolkit_extract\sratoolkit.3.4.1-win64\bin;%PROJECT_ROOT%\tools\ncbi-magicblast-1.7.2\bin;%PATH%"
echo D-project Windows-native bioinformatics toolchain is now on PATH for this terminal.
echo Project root: %PROJECT_ROOT%
echo.
prefetch --version
fasterq-dump --version
vdb-dump --version
magicblast -version
makeblastdb -version
