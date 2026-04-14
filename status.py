import os
from pathlib import Path
import sys
import hashlib
import json

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

if not Path(os.path.join(sccs_dir, "commit_file_hash.json")).is_file():
    print("Commit file hash JSON not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(os.path.join(sccs_dir, "commit_messages")).is_dir():
    print("Commit messages directory not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(os.path.join(sccs_dir, "commit_messages.json")).is_file():
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

if not Path(os.path.join(sccs_dir, "history", "commit_history.json")).is_file():
    print("History file not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(path).is_file():
    print("Docx file not found. Re-initialize SCCS for this file with 'sccs init <file_path>'")
    sys.exit(1)

try:
    with open(path, "rb") as f:
        hasher = hashlib.sha256()
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
        hashed_file = hasher.hexdigest()
except Exception as e:
    print(f"Error processing .docx file: {e}")
    sys.exit(1)

# get the latest commit filename hash from commit history
history_path = os.path.join(directory_path, ".sccs", "history", "commit_history.json")
if not Path(history_path).is_file():
    print("History file not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

try:
    with open(history_path, "r", encoding="utf-8", newline="\n") as history_file:
        history = json.load(history_file)
        latest_commit_hash = history["latest_commit"]
except (json.JSONDecodeError, KeyError, TypeError):
    print("History file is missing or corrupted. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not latest_commit_hash:
    print("History file is missing the latest commit information. Please reinitialize SCCS for this file.") 
    sys.exit(1)

# get the hash of the latest committed file
latest_commit_file_hash_path = os.path.join(directory_path, ".sccs", "commit_file_hash", "commit_file_hash.json")
if not Path(latest_commit_file_hash_path).is_file():
    print("Latest commit file hash not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

try:
    with open(latest_commit_file_hash_path, "r", encoding="utf-8", newline="\n") as f:
        commit_file_hash_data = json.load(f)
        latest_commit_file_hash = commit_file_hash_data.get(latest_commit_hash)
except (json.JSONDecodeError, KeyError, TypeError, OSError) as e:
    print("Latest commit file hash is missing or corrupted. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not latest_commit_file_hash:
    print("Latest commit file hash is missing. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if hashed_file == latest_commit_file_hash:
    print("No changes detected since the latest commit. Nothing to commit.")
    sys.exit(0)

else: 
    print("Changes detected since the latest commit. You can proceed with committing these changes.")
    sys.exit(0)