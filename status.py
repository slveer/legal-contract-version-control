import os
from pathlib import Path
import sys
import hashlib
import json

# Get user inputted path argument
path = sys.argv[2] if len(sys.argv) > 2 else None

# Strip .docx extension from the file name to create a directory
# Because sccs init moves the file into the directory, update the path to point to the moved file
if path: 

    directory_path = Path(path).with_suffix("")

    # if directory basename = parent directory name (eg: user/file/file), use parent directory (eg: user/file).
    if directory_path.name == directory_path.parent.name:
        directory_path = directory_path.parent

    # Set path correctly, whether it was correct in the first place or not
    path = os.path.join(directory_path, os.path.basename(path))

    if not Path(path).is_file():
        print("File not found. Please provide a valid file path.")
        sys.exit(1)
else:
    print("No file path provided")
    sys.exit(1)
if path and Path(path).suffix.lower() == ".docx" and Path(path).is_file():
    try:
        with open(path, "rb") as f:
            hasher = hashlib.sha256()
            for chunk in iter(lambda: f.read(65536), b""):
                hasher.update(chunk)
            hashed_file = hasher.hexdigest()
    except Exception as e:
        print(f"Error processing .docx file: {e}")
        sys.exit(1)

# Check if the directory contains an SCCS initialization
elif not Path(os.path.join(directory_path, ".sccs")).is_dir():
    print("This file has not been initialized with SCCS.")
    print("Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)



# if not, exit  
else: 
    print("Invalid file path, make sure the file exists and is a .docx file")
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