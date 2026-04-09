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

if "%command%"=="open" (
    set "script_directory=%~dp0"
    python "%script_directory%open.py" %*
    exit /b !errorlevel!
)

if "%command%"=="log" (
    set "script_directory=%~dp0"
    python "%script_directory%log.py" %*
    exit /b !errorlevel!
)
echo Unknown command: %command%
echo Invalid command. Please use either "init", "commit", "open", or "log", along with required arguments
exit /b 1