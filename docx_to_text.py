import subprocess
from pathlib import Path
import sys
import docx2txt 
import hashlib
from datetime import datetime

# Get user inputted path argument
path = sys.argv[2] if len(sys.argv) > 2 else None

# Check if the path ends with .docx and exists
if path and path.endswith(".docx") and Path(path).is_file():
    docx_to_txt = docx2txt.process(path)

# if not, exit  
else: 
    print("Invalid file path, make sure the file exists and is a .docx file")
    sys.exit(1)

# Strip .docx extension from the file name to create a directory
directory_path = Path(path).with_suffix('')

# Check if the directory already contains an SCCS initialization
if Path(f"{directory_path}/.sccs").is_dir():
    print("This file has already been initialized with SCCS")
    sys.exit(1)

# Get user inputted name and email
name = input("Enter your name: ")
email = input("Enter your email: ")

# Generate a SHA-256 hash for the initial commit
sha_hash = hashlib.sha256(f'{datetime.now().isoformat()}/initial_version/{name}/{email}'.encode()).hexdigest()

# Create needed directories
subprocess.run(["mkdir", "-p", directory_path])
subprocess.run(["mv", path, directory_path])
subprocess.run(["mkdir", "-p", f"{directory_path}/.sccs"])
subprocess.run(["mkdir", "-p", f"{directory_path}/.sccs/commits"])
subprocess.run(["mkdir", "-p", f"{directory_path}/.sccs/history"])
subprocess.run(["mkdir", "-p", f"{directory_path}/.sccs/commit_messages"])
subprocess.run(["mkdir", "-p", f"{directory_path}/.sccs/config"])

# Add info to the directories, JSON
with open(f"{directory_path}/.sccs/commits/{sha_hash}.txt", "w") as f:
    f.write(docx_to_txt)

history_data = {
    "initial commit": f"{sha_hash}.txt"
}

with open(f"{directory_path}/.sccs/history/commit_history.json", "w") as f:
    f.write(history_data)

commit_message_data = {
    f"{sha_hash}.txt": "initial commit (This is a default commit message for initial version)"
}

with open(f"{directory_path}/.sccs/commit_messages/commit_messages.json", "w") as f:
    f.write(commit_message_data)

config_data = {
    "name": f"{name}",
    "email": f"{email}"
}

with open(f"{directory_path}/.sccs/config/config.json", "w") as f:
    f.write(config_data)