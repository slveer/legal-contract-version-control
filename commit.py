import os
from pathlib import Path
import shutil
import sys
import hashlib
from datetime import datetime
import json
import mammoth
from default_css_styles import styles
from sccs_layout_check import check_sccs, path, directory_path, wrap_html

def hash_current_docx_binary():
    try:
        with open(path, "rb") as f:
                hasher = hashlib.sha256()
                for chunk in iter(lambda: f.read(65536), b""):
                    hasher.update(chunk)
                hashed_file = hasher.hexdigest()
    except Exception as e:
        print(f"Error processing .docx file: {e}")
        sys.exit(1)
    print(f"Error processing .docx file: {e}")
    sys.exit(1)
    return hashed_file

def convert_docx_to_html():
    try: 
        with open(path, "rb") as f:
            result = mammoth.convert_to_html(f)
            html = result.value
    except Exception as e:
        print(f"Error converting .docx to HTML: {e}")
        sys.exit(1)
        return html

check_sccs()

hash_docx_binary = hash_current_docx_binary()
docx_html = convert_docx_to_html()

# Get name and email entered on init
config_path = os.path.join(directory_path, ".sccs", "config", "config.json")
if not Path(config_path).is_file():
    print("Configuration file not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

with open(config_path, "r", encoding="utf-8", newline="\n") as config_file:
    config = json.load(config_file)
    name = config.get("name")
    email = config.get("email")

# Get commit message
commit_message = input("Enter commit message: ").strip()

if commit_message == "":
    print("Commit message cannot be empty.")
    sys.exit(1)

timestamp = datetime.now().isoformat()

# Get parent hash

#Get current branch
current_branch_path = os.path.join(directory_path, ".sccs", "current_branch", "current_branch.json")
if not Path(current_branch_path).is_file():
    print("Current branch file not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

with open(current_branch_path, "r", encoding="utf-8", newline="\n") as current_branch_file:
    current_branch = json.load(current_branch_file).get("current_branch")


history_path = os.path.join(directory_path, ".sccs", "branches", current_branch, "history", "commit_history.json")
if not Path(history_path).is_file():
    print("History file not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

try:
    with open(history_path, "r", encoding="utf-8", newline="\n") as history_file:
    
        history = json.load(history_file)
        parent_hash = history["history"].get("latest_commit")

except Exception as e:
    print(f"Error retrieving JSON from history file: {e}")
    sys.exit(1)


# Generate commit hash from time, message, name, email, and previous commit hash
sha_hash = hashlib.sha256(f'{timestamp}/{commit_message}/{name}/{email}/{parent_hash}'.encode()).hexdigest()

shutil.copy2(os.path.join(directory_path, Path(path).name) , os.path.join(directory_path, ".sccs", "objects", "docx", f"{sha_hash}.docx"))

with open(os.path.join(directory_path, ".sccs", "objects", "html", f"{sha_hash}.html"), "w", encoding="utf-8", newline="\n") as f:
    f.write(styles + docx_html)

with open(os.path.join(directory_path, ".sccs", "objects", "view_html", f"{sha_hash}.html"), "w", encoding="utf-8", newline="\n") as f:
    f.write(wrap_html(docx_html))    

# Update history
history["history"]["latest_commit"] = f"{sha_hash}"
history["history"]["latest_commit_number"] = history["history"].get("latest_commit_number", 0) + 1
history["history"]["commit_order"][str(history["history"]["latest_commit_number"])] = f"{sha_hash}"

history["log"][f"{sha_hash}"] = {
    "timestamp": timestamp,
    "author": f"{name} <{email}>",
    "message": commit_message
}

with open(history_path, "w", encoding="utf-8", newline="\n") as history_file:
    json.dump(history, history_file, indent=4)

# Update commit messages
commit_messages_path = os.path.join(directory_path, ".sccs", "commit_messages", "commit_messages.json")
if not Path(commit_messages_path).is_file():
    print("Commit messages file not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

with open(commit_messages_path, "r", encoding="utf-8", newline="\n") as commit_messages_file:
    messages = json.load(commit_messages_file)

messages[f"{sha_hash}"] = f"{commit_message}"

with open(commit_messages_path, "w", encoding="utf-8", newline="\n") as commit_messages_file:
    json.dump(messages, commit_messages_file, indent=4)



# Update commit file hash
commit_file_hash_path = os.path.join(directory_path, ".sccs", "branches", current_branch, "commit_file_hash", "commit_file_hash.json")
if not Path(commit_file_hash_path).is_file():
    print("Commit file hash not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

try: 
    with open(commit_file_hash_path, "r", encoding="utf-8", newline="\n") as f:
        commit_file_hash = json.load(f)

except (json.JSONDecodeError, KeyError, TypeError, OSError) as e:
    print("Commit file hash is missing or corrupted. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

commit_file_hash[f"{sha_hash}"] = hash_docx_binary

with open(commit_file_hash_path, "w", encoding="utf-8", newline="\n") as f:
    json.dump(commit_file_hash, f, indent=4)

print(f"Commit {sha_hash} created successfully.")