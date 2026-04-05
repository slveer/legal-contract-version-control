import os
import shutil
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
else:
    print("No file path provided")
    sys.exit(1)

# Check if the directory already contains an SCCS initialization
if Path(os.path.join(directory_path, ".sccs")).is_dir():
    print("This file has already been initialized with SCCS")
    sys.exit(1)

# Check if the path ends with .docx and exists
elif path and Path(path).suffix.lower() == ".docx" and Path(path).is_file():
    try:
        docx_to_txt = docx2txt.process(path)
    except Exception as e:
        print(f"Error processing .docx file: {e}")
        sys.exit(1)

# if not, exit  
else: 
    print("Invalid file path, make sure the file exists and is a .docx file")
    sys.exit(1)

# Get user inputted name and email
name = input("Enter your name: ")
email = input("Enter your email: ")

# Generate a SHA-256 hash for the initial commit
sha_hash = hashlib.sha256(f'{datetime.now().isoformat()}/initial_version/{name}/{email}'.encode()).hexdigest()

# Create needed directories
os.makedirs(directory_path, exist_ok=True)
shutil.move(path, directory_path)
os.makedirs(os.path.join(directory_path, ".sccs"), exist_ok=True)
os.makedirs(os.path.join(directory_path, ".sccs", "commits"), exist_ok=True)
os.makedirs(os.path.join(directory_path, ".sccs", "history"), exist_ok=True)
os.makedirs(os.path.join(directory_path, ".sccs", "commit_messages"), exist_ok=True)
os.makedirs(os.path.join(directory_path, ".sccs", "config"), exist_ok=True)
# Add info to the directories, JSON
with open(os.path.join(directory_path, ".sccs", "commits", f"{sha_hash}.txt"), "w", encoding="utf-8", newline="\n") as f:
    f.write(docx_to_txt)

history_data = {
    "initial_commit": f"{sha_hash}.txt",
    "latest_commit": f"{sha_hash}.txt",
    "latest_commit_number": 1,
    "commit_order": {
        "1": f"{sha_hash}.txt"
    }
}

with open(os.path.join(directory_path, ".sccs", "history", "commit_history.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(history_data, f, indent=4)

commit_message_data = {
    f"{sha_hash}.txt": "initial commit (This is a default commit message for initial version)"
}

with open(os.path.join(directory_path, ".sccs", "commit_messages", "commit_messages.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(commit_message_data, f, indent=4)

config_data = {
    "name": f"{name}",
    "email": f"{email}"
}

with open(os.path.join(directory_path, ".sccs", "config", "config.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(config_data, f, indent=4)

print("SCCS initialization complete.")
