@echo off
setlocal enabledelayedexpansion

set "command=%1"

if "%command%"=="init" (
    set "script_directory=%~dp0"
    python "%script_directory%init.py" %*
    exit /b !errorlevel!
)

if "%command%"=="commit" (
    set "script_directory=%~dp0"
    python "%script_directory%commit.py" %*
    exit /b !errorlevel!
)

echo Unknown command: %command%
echo Invalid command. Please use either "init" or "commit", along with required arguments
exit /b 1