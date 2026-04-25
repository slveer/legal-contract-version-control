import os
import shutil
from pathlib import Path
import sys
import hashlib
from datetime import datetime
import json
import mammoth
from default_css_styles import styles
from sccs_layout_check import wrap_html
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
        with open(path, "rb") as f:
            hasher = hashlib.sha256()
            for chunk in iter(lambda: f.read(65536), b""):
                hasher.update(chunk)
            hashed_file = hasher.hexdigest()
    except Exception as e:
        print(f"Error processing .docx file: {e}")
        sys.exit(1)
    try: 
        with open(path, "rb") as f:
            result = mammoth.convert_to_html(f)
            html = result.value
    except Exception as e:
        print(f"Error converting .docx to HTML: {e}")
        sys.exit(1)

# if not, exit  

else: 
    print("Invalid file path, make sure the file exists and is a .docx file")
    sys.exit(1)

# Get user inputted name and email
name = input("Enter your name: ")
email = input("Enter your email: ")

timestamp = datetime.now().isoformat()
initial_commit_message = "initial commit (This is a default commit message for initial version)"

# Generate a SHA-256 hash for the initial commit
sha_hash = hashlib.sha256(f'{timestamp}/initial_version/{name}/{email}'.encode()).hexdigest()

# Create needed directories
os.makedirs(directory_path, exist_ok=True)
shutil.move(path, directory_path)
os.makedirs(os.path.join(directory_path, ".sccs"), exist_ok=True)
os.makedirs(os.path.join(directory_path, ".sccs", "objects"), exist_ok=True)
os.makedirs(os.path.join(directory_path, ".sccs", "objects", "docx"), exist_ok=True)
os.makedirs(os.path.join(directory_path, ".sccs", "objects", "html"), exist_ok=True)
os.makedirs(os.path.join(directory_path, ".sccs", "objects", "view_html"), exist_ok=True)
os.makedirs(os.path.join(directory_path, ".sccs", "history"), exist_ok=True)
os.makedirs(os.path.join(directory_path, ".sccs", "commit_messages"), exist_ok=True)
os.makedirs(os.path.join(directory_path, ".sccs", "config"), exist_ok=True)
os.makedirs(os.path.join(directory_path, ".sccs", "commit_file_hash"), exist_ok=True)
# Add info to the directories, JSON

shutil.copy2(os.path.join(directory_path, Path(path).name), os.path.join(directory_path, ".sccs", "objects", "docx", f"{sha_hash}.docx"))

with open(os.path.join(directory_path, ".sccs", "objects", "html", f"{sha_hash}.html"), "w", encoding="utf-8", newline="\n") as f:
    f.write(styles + html)

with open(os.path.join(directory_path, ".sccs", "objects", "view_html", f"{sha_hash}.html"), "w", encoding="utf-8", newline="\n") as f:
    f.write(wrap_html(html))

history_data = {
    "initial_commit": f"{sha_hash}",
    "latest_commit": f"{sha_hash}",
    "latest_commit_number": 1,
    "commit_order": {
        "1": f"{sha_hash}"
    }
}

with open(os.path.join(directory_path, ".sccs", "history", "commit_history.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(history_data, f, indent=4)

log_data = {
    f"{sha_hash}": {
        "timestamp": timestamp,
        "author": f"{name} <{email}>",
        "message": initial_commit_message
    }
}
     
with open(os.path.join(directory_path, ".sccs", "history", "commit_log.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(log_data, f, indent=4)

commit_message_data = {
    f"{sha_hash}": initial_commit_message
}

with open(os.path.join(directory_path, ".sccs", "commit_messages", "commit_messages.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(commit_message_data, f, indent=4)

config_data = {
    "name": f"{name}",
    "email": f"{email}"
}

with open(os.path.join(directory_path, ".sccs", "config", "config.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(config_data, f, indent=4)

commit_file_hash_data = {
    f"{sha_hash}": hashed_file
}

with open (os.path.join(directory_path, ".sccs", "commit_file_hash", f"commit_file_hash.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(commit_file_hash_data, f, indent=4)
print("SCCS initialization complete.")
