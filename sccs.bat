@echo off
setlocal enabledelayedexpansion

set "command=%1"

if "%command%"=="init" (
    python init.py %*
    exit /b %errorlevel%
)

if "%command%"=="commit" (
    python commit.py %*
    exit /b %errorlevel%
)
else (
    echo Invalid Command. Please use either "init" or "commit", along with required arguments
    exit /b 1
)

@REM Instructions to set up sccs.bat in CLI on Windows:

@REM Search "environment variables" in the Start menu
@REM Click "Edit the system environment variables"
@REM Click "Environment Variables"
@REM Under "User variables", find Path and click Edit
@REM Add the folder where sccs.bat lives, e.g. C:\Users\YOUR_USERNAME\bin