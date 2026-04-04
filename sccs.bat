#!/usr/bin/env python3 

import sys
import subprocess

command = sys.argv[1] if len(sys.argv) > 1 else None

if command == "init":
    subprocess.run(["python3", "init.py"] + sys.argv[1:]) 

if command == "commit":
    subprocess.run(["python3", "commit.py"] + sys.argv[1:])

@REM # Instructions to set up sccs.bat in CLI on Windows

@REM Search "environment variables" in the Start menu
@REM Click "Edit the system environment variables"
@REM Click "Environment Variables"
@REM Under "User variables", find Path and click Edit
@REM Add the folder where sccs.bat lives, e.g. C:\Users\YOUR_USERNAME\bin