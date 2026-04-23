import os
from pathlib import Path
import shutil
import sys
import docx2txt 
import hashlib
from datetime import datetime
import json
import mammoth
from default_css_styles import styles
from sccs_layout_check import check_sccs, wrap_html, path, directory_path


check_sccs()

try: 
    commit = docx2txt.process(path)
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
commit_message = input("Enter commit message: ")

timestamp = datetime.now().isoformat()

# Get parent hash
history_path = os.path.join(directory_path, ".sccs", "history", "commit_history.json")
if not Path(history_path).is_file():
    print("History file not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

with open(history_path, "r", encoding="utf-8", newline="\n") as history_file:
    history = json.load(history_file)
    parent_hash = history["latest_commit"]

# Generate commit hash from time, message, name, email, and previous commit hash
sha_hash = hashlib.sha256(f'{timestamp}/{commit_message}/{name}/{email}/{parent_hash}'.encode()).hexdigest()

# Write .txt file
with open(os.path.join(directory_path, ".sccs", "commits", "txt-commits", f"{sha_hash}.txt"), "w", encoding="utf-8", newline="\n") as f:
    f.write(commit)

shutil.copy2(os.path.join(directory_path, Path(path).name) , os.path.join(directory_path, ".sccs", "commits", "docx-commits", f"{sha_hash}.docx"))

with open(os.path.join(directory_path, ".sccs", "commits", "html-commits", f"{sha_hash}.html"), "w", encoding="utf-8", newline="\n") as f:
    f.write(wrap_html(html))

# Update history
history["latest_commit"] = f"{sha_hash}"
history["latest_commit_number"] = history.get("latest_commit_number", 0) + 1
history["commit_order"][str(history["latest_commit_number"])] = f"{sha_hash}"
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

# Update commit log
commit_log_path = os.path.join(directory_path, ".sccs", "history", "commit_log.json")
if not Path(commit_log_path).is_file():
    print("Commit log file not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

with open(commit_log_path, "r", encoding="utf-8", newline="\n") as commit_log_file:
    log = json.load(commit_log_file)

log[f"{sha_hash}"] = {
    "timestamp": timestamp,
    "author": f"{name} <{email}>",
    "message": commit_message
}

with open(commit_log_path, "w", encoding="utf-8", newline="\n") as commit_log_file:
    json.dump(log, commit_log_file, indent=4)

# Update commit file hash
commit_file_hash_path = os.path.join(directory_path, ".sccs", "commit_file_hash", "commit_file_hash.json")
if not Path(commit_file_hash_path).is_file():
    print("Commit file hash not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

try: 
    with open(commit_file_hash_path, "r", encoding="utf-8", newline="\n") as f:
        commit_file_hash = json.load(f)

except (json.JSONDecodeError, KeyError, TypeError, OSError) as e:
    print("Commit file hash is missing or corrupted. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

commit_file_hash[f"{sha_hash}"] = hashed_file

with open(commit_file_hash_path, "w", encoding="utf-8", newline="\n") as f:
    json.dump(commit_file_hash, f, indent=4)

print(f"Commit {sha_hash} created successfully.")