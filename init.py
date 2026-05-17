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
entered_document_path = sys.argv[2] if len(sys.argv) > 2 else None
document_directory_path = Path(entered_document_path).with_suffix('')

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

def check_for_prev_init():
    if Path(os.path.join(document_directory_path, ".sccs")).is_dir():
        print("This file has already been initialized with SCCS")
        sys.exit(1)

def check_file_requirements():
    if not entered_document_path and Path(entered_document_path).suffix.lower() == ".docx" and Path(entered_document_path).is_file():
        print("Invalid file path, make sure the file exists and is a .docx file")
        sys.exit(1)

check_if_arg_entered(entered_document_path)

check_for_prev_init()

try:
    with open(entered_document_path, "rb") as f:
        hasher = hashlib.sha256()
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
        hashed_file = hasher.hexdigest()
except Exception as e:
    print(f"Error processing .docx file: {e}")
    sys.exit(1)
try: 
    with open(entered_document_path, "rb") as f:
        result = mammoth.convert_to_html(f)
        html = result.value
except Exception as e:
    print(f"Error converting .docx to HTML: {e}")
    sys.exit(1)

# Get user inputted name and email
config_user_name = ask_config_input("name")

config_user_email = ask_config_input("email")

current_timestamp = datetime.now().isoformat()

initial_commit_message = "initial commit (This is a default commit message for initial version)"

# Generate a SHA-256 hash for the initial commit
sha_hash = hashlib.sha256(f'{current_timestamp}/initial_version/{config_user_name}/{config_user_email}'.encode()).hexdigest()

# Create needed directories
os.makedirs(document_directory_path, exist_ok=True)
shutil.move(entered_document_path, document_directory_path)
os.makedirs(os.path.join(document_directory_path, ".sccs"), exist_ok=True)
os.makedirs(os.path.join(document_directory_path, ".sccs", "objects"), exist_ok=True)
os.makedirs(os.path.join(document_directory_path, ".sccs", "objects", "docx"), exist_ok=True)
os.makedirs(os.path.join(document_directory_path, ".sccs", "objects", "html"), exist_ok=True)
os.makedirs(os.path.join(document_directory_path, ".sccs", "objects", "view_html"), exist_ok=True)
os.makedirs(os.path.join(document_directory_path, ".sccs", "branches"), exist_ok=True)
os.makedirs(os.path.join(document_directory_path, ".sccs", "branches", "main"), exist_ok=True)
os.makedirs(os.path.join(document_directory_path, ".sccs", "branches", "main", "history"), exist_ok=True)
os.makedirs(os.path.join(document_directory_path, ".sccs", "branches", "main", "commit_file_hash"), exist_ok=True)
os.makedirs(os.path.join(document_directory_path, ".sccs", "commit_messages"), exist_ok=True)
os.makedirs(os.path.join(document_directory_path, ".sccs", "config"), exist_ok=True)
os.makedirs(os.path.join(document_directory_path, ".sccs", "current_branch"), exist_ok=True)
# Add info to the directories, JSON

shutil.copy2(os.path.join(document_directory_path, Path(entered_document_path).name), os.path.join(document_directory_path, ".sccs", "objects", "docx", f"{sha_hash}.docx"))

with open(os.path.join(document_directory_path, ".sccs", "objects", "html", f"{sha_hash}.html"), "w", encoding="utf-8", newline="\n") as f:
    f.write(styles + html)

with open(os.path.join(document_directory_path, ".sccs", "objects", "view_html", f"{sha_hash}.html"), "w", encoding="utf-8", newline="\n") as f:
    f.write(wrap_html(html))

HISTORY_DATA = {
    "history": {
    "initial_commit": f"{sha_hash}",
    "latest_commit": f"{sha_hash}",
    "latest_commit_number": 1,
    "commit_order": {
        "1": f"{sha_hash}"
    }
    },
    "log": {
    f"{sha_hash}": {
    "timestamp": current_timestamp,
    "author": f"{config_user_name} <{config_user_email}>",
    "message": initial_commit_message
    }
    }
}

with open(os.path.join(document_directory_path, ".sccs", "branches", "main", "history", "commit_history.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(HISTORY_DATA, f, indent=4)

COMMIT_MESSAGE_DATA = {
    f"{sha_hash}": initial_commit_message
}

with open(os.path.join(document_directory_path, ".sccs", "commit_messages", "commit_messages.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(COMMIT_MESSAGE_DATA, f, indent=4)

CONFIG_DATA = {
    "name": f"{config_user_name}",
    "email": f"{config_user_email}"
}

with open(os.path.join(document_directory_path, ".sccs", "config", "config.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(CONFIG_DATA, f, indent=4)

COMMIT_FILE_HASH_DATA = {
    f"{sha_hash}": hashed_file
}

with open (os.path.join(document_directory_path, ".sccs", "branches", "main", "commit_file_hash", "commit_file_hash.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(COMMIT_FILE_HASH_DATA, f, indent=4)

with open(os.path.join(document_directory_path, ".sccs", "current_branch", "current_branch.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump({
        "current_branch": "main",
        "branches": ["main"]
    }, f, indent=4)

print("SCCS initialization complete.")
