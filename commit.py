import os
from pathlib import Path
import sys
import docx2txt 
import hashlib
from datetime import datetime
import json


# Get user inputted path argument
path = sys.argv[2] if len(sys.argv) > 2 else None

# Strip .docx extension from the file name to create a directory
if path: 
    directory_path = Path(path).with_suffix('')
    # Because sccs init moves the file into the directory, update the path to point to the moved file
    path = os.path.join(directory_path, os.path.basename(path))
else:
    print("No file path provided")
    sys.exit(1)

# Check if the directory contains an SCCS initialization
if not Path(os.path.join(directory_path, ".sccs")).is_dir():
    print("This file has not been initialized with SCCS.")
    print("Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

elif path and Path(path).suffix.lower() == ".docx" and Path(path).is_file():
    try: 
        commit = docx2txt.process(path)
    except Exception as e:
        print(f"Error processing .docx file: {e}")
        sys.exit(1)

# if not, exit  
else: 
    print("Invalid file path, make sure the file exists and is a .docx file")
    sys.exit(1)

# Get name and email entered on init
config_path = os.path.join(directory_path, ".sccs", "config", "config.json")
if not Path(config_path).is_file():
    print("Configuration file not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

with open(config_path, "r") as config_file:
    config = json.load(config_file)
    name = config.get("name")
    email = config.get("email")

# Get commit message
commit_message = input("Enter commit message: ")

# Get parent hash
history_path = os.path.join(directory_path, ".sccs", "history", "commit_history.json")
if not Path(history_path).is_file():
    print("History file not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

with open(history_path, "r") as history_file:
    history = json.load(history_file)
    parent_hash = history.get("latest_commit")

# Generate commit hash from time, message, name, email, and previous commit hash
sha_hash = hashlib.sha256(f'{datetime.now().isoformat()}/{commit_message}/{name}/{email}/{parent_hash}'.encode()).hexdigest()

# Write .txt file
with open(os.path.join(directory_path, ".sccs", "commits", f"{sha_hash}.txt"), "w", encoding="utf-8", newline="\n") as f:
    f.write(commit)

# Update history
history["latest_commit"] = f"{sha_hash}.txt"
history["latest_commit_number"] = history.get("latest_commit_number", 0) + 1
history["commit_order"][str(history["latest_commit_number"])] = f"{sha_hash}.txt"
with open(history_path, "w", encoding="utf-8", newline="\n") as history_file:
    json.dump(history, history_file, indent=4)

# Update commit messages
commit_messages_path = os.path.join(directory_path, ".sccs", "commit_messages", "commit_messages.json")
if not Path(commit_messages_path).is_file():
    print("Commit messages file not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

with open(commit_messages_path, "r", encoding="utf-8", newline="\n") as commit_messages_file:
    messages = json.load(commit_messages_file)

messages[f"{sha_hash}.txt"] = f"{commit_message}"

with open(commit_messages_path, "w", encoding="utf-8", newline="\n") as commit_messages_file:
    json.dump(messages, commit_messages_file, indent=4)

print(f"Commit {sha_hash} created successfully.")