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
PATH = sys.argv[2] if len(sys.argv) > 2 else None
DIRECTORY_PATH = Path(PATH).with_suffix('')

# Strip .docx extension from the file name to create a directory
def check_if_arg_entered(arg):
    if not arg:
        print("No file path provided")
        sys.exit(1)

def ask_config_input(data):
    data_value = input(f"Enter your {data}: ").strip()
    if data_value == "":
        print(f"{data} cannot be empty.")
        sys.exit(1)
    else:
        return data_value

check_if_arg_entered(PATH)

# Check if the directory already contains an SCCS initialization
if Path(os.path.join(DIRECTORY_PATH, ".sccs")).is_dir():
    print("This file has already been initialized with SCCS")
    sys.exit(1)

# Check if the path ends with .docx and exists
elif PATH and Path(PATH).suffix.lower() == ".docx" and Path(PATH).is_file():
    try:
        with open(PATH, "rb") as f:
            hasher = hashlib.sha256()
            for chunk in iter(lambda: f.read(65536), b""):
                hasher.update(chunk)
            hashed_file = hasher.hexdigest()
    except Exception as e:
        print(f"Error processing .docx file: {e}")
        sys.exit(1)
    try: 
        with open(PATH, "rb") as f:
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
NAME = ask_config_input("name")

EMAIL = ask_config_input("email")

TIMESTAMP = datetime.now().isoformat()
INITIAL_COMMIT_MESSAGE = "initial commit (This is a default commit message for initial version)"

# Generate a SHA-256 hash for the initial commit
SHA_HASH = hashlib.sha256(f'{TIMESTAMP}/initial_version/{NAME}/{EMAIL}'.encode()).hexdigest()

# Create needed directories
os.makedirs(DIRECTORY_PATH, exist_ok=True)
shutil.move(PATH, DIRECTORY_PATH)
os.makedirs(os.path.join(DIRECTORY_PATH, ".sccs"), exist_ok=True)
os.makedirs(os.path.join(DIRECTORY_PATH, ".sccs", "objects"), exist_ok=True)
os.makedirs(os.path.join(DIRECTORY_PATH, ".sccs", "objects", "docx"), exist_ok=True)
os.makedirs(os.path.join(DIRECTORY_PATH, ".sccs", "objects", "html"), exist_ok=True)
os.makedirs(os.path.join(DIRECTORY_PATH, ".sccs", "objects", "view_html"), exist_ok=True)
os.makedirs(os.path.join(DIRECTORY_PATH, ".sccs", "branches"), exist_ok=True)
os.makedirs(os.path.join(DIRECTORY_PATH, ".sccs", "branches", "main"), exist_ok=True)
os.makedirs(os.path.join(DIRECTORY_PATH, ".sccs", "branches", "main", "history"), exist_ok=True)
os.makedirs(os.path.join(DIRECTORY_PATH, ".sccs", "branches", "main", "commit_file_hash"), exist_ok=True)
os.makedirs(os.path.join(DIRECTORY_PATH, ".sccs", "commit_messages"), exist_ok=True)
os.makedirs(os.path.join(DIRECTORY_PATH, ".sccs", "config"), exist_ok=True)
os.makedirs(os.path.join(DIRECTORY_PATH, ".sccs", "current_branch"), exist_ok=True)
# Add info to the directories, JSON

shutil.copy2(os.path.join(DIRECTORY_PATH, Path(PATH).name), os.path.join(DIRECTORY_PATH, ".sccs", "objects", "docx", f"{SHA_HASH}.docx"))

with open(os.path.join(DIRECTORY_PATH, ".sccs", "objects", "html", f"{SHA_HASH}.html"), "w", encoding="utf-8", newline="\n") as f:
    f.write(styles + html)

with open(os.path.join(DIRECTORY_PATH, ".sccs", "objects", "view_html", f"{SHA_HASH}.html"), "w", encoding="utf-8", newline="\n") as f:
    f.write(wrap_html(html))

HISTORY_DATA = {
    "history": {
    "initial_commit": f"{SHA_HASH}",
    "latest_commit": f"{SHA_HASH}",
    "latest_commit_number": 1,
    "commit_order": {
        "1": f"{SHA_HASH}"
    }
    },
    "log": {
    f"{SHA_HASH}": {
    "timestamp": TIMESTAMP,
    "author": f"{NAME} <{EMAIL}>",
    "message": INITIAL_COMMIT_MESSAGE
    }
    }
}

with open(os.path.join(DIRECTORY_PATH, ".sccs", "branches", "main", "history", "commit_history.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(HISTORY_DATA, f, indent=4)

COMMIT_MESSAGE_DATA = {
    f"{SHA_HASH}": INITIAL_COMMIT_MESSAGE
}

with open(os.path.join(DIRECTORY_PATH, ".sccs", "commit_messages", "commit_messages.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(COMMIT_MESSAGE_DATA, f, indent=4)

CONFIG_DATA = {
    "name": f"{NAME}",
    "email": f"{EMAIL}"
}

with open(os.path.join(DIRECTORY_PATH, ".sccs", "config", "config.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(CONFIG_DATA, f, indent=4)

COMMIT_FILE_HASH_DATA = {
    f"{SHA_HASH}": hashed_file
}

with open (os.path.join(DIRECTORY_PATH, ".sccs", "branches", "main", "commit_file_hash", "commit_file_hash.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(COMMIT_FILE_HASH_DATA, f, indent=4)

with open(os.path.join(DIRECTORY_PATH, ".sccs", "current_branch", "current_branch.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump({
        "current_branch": "main",
        "branches": ["main"]
    }, f, indent=4)

print("SCCS initialization complete.")
