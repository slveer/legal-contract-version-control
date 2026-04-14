import json
from pathlib import Path
import os
import sys



directory_path = os.getcwd()

path = os.path.join(directory_path, f"{os.path.basename(directory_path)}.docx")

sccs_dir = os.path.join(directory_path, ".sccs")

if not Path(sccs_dir).is_dir():
    print("This file has not been initialized with SCCS.")
    print("Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(os.path.join(sccs_dir, "commit_file_hash")).is_dir():
    print("Commit file hash directory not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(os.path.join(sccs_dir, "commit_file_hash", "commit_file_hash.json")).is_file():
    print("Commit file hash JSON not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(os.path.join(sccs_dir, "commit_messages")).is_dir():
    print("Commit messages directory not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(os.path.join(sccs_dir, "commit_messages", "commit_messages.json")).is_file():
    print("Commit messages JSON not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(os.path.join(sccs_dir, "commits")).is_dir():
    print("Commits directory not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(os.path.join(sccs_dir, "commits", "txt-commits")).is_dir():
    print("Text commits directory not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(os.path.join(sccs_dir, "commits", "docx-commits")).is_dir():
    print("Docx commits directory not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(os.path.join(sccs_dir, "config")).is_dir():
    print("Config directory not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(os.path.join(sccs_dir, "config", "config.json")).is_file():
    print("Config file not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(os.path.join(sccs_dir, "history")).is_dir():
    print("History directory not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(os.path.join(sccs_dir, "history", "commit_history.json")).is_file():
    print("History file not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(path).is_file():
    print("Docx file not found. Re-initialize SCCS for this file with 'sccs init <file_path>'")
    sys.exit(1)

# Get JSON log data
log_path = os.path.join(directory_path, ".sccs", "history", "commit_log.json")
if not Path(log_path).is_file():
    print("Log file not found. Please make sure the file has been initialized with SCCS.")
    sys.exit(1)

with open(log_path, "r", encoding="utf-8", newline="\n") as log_file:
    log_data = json.load(log_file)
# Print log data
for entry in log_data:
    print(
        "------------------------------\n"
        f"Commit File: {entry}\n"
        f"Author: {log_data[entry]['author']}\n"
        f"Date: {log_data[entry]['timestamp']}\n"
        f"Message: {log_data[entry]['message']}\n"
        "-----------------------------"
    )