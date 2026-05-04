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

check_sccs()

def hash_current_docx_binary():
    """
    Compute the SHA-256 hex digest of the current `.docx` file referenced by the module-level `path`.
    
    On I/O or other failure, prints an error message and exits the process with status 1.
    
    Returns:
        str: SHA-256 hex digest of the `.docx` file contents.
    """
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
    """
    Convert the current DOCX file at `path` into an HTML string.
    
    Returns:
        html (str): The converted HTML content of the DOCX file.
    """
    try: 
        with open(path, "rb") as f:
            result = mammoth.convert_to_html(f)
            html = result.value
    except Exception as e:
        print(f"Error converting .docx to HTML: {e}")
        sys.exit(1)
        return html

def get_obj_from_config(object):
    # Get name and email entered on init
    """
    Retrieve a value from the SCCS configuration by key.
    
    If the SCCS config file is missing, prints an initialization instruction and exits with status 1.
    
    Parameters:
        object (str): The configuration key to look up (e.g., "name" or "email").
    
    Returns:
        The value associated with the given key from the config JSON, or `None` if the key is not present.
    """
    config_path = os.path.join(directory_path, ".sccs", "config", "config.json")
    if not Path(config_path).is_file():
        print("Configuration file not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8", newline="\n") as config_file:
        config = json.load(config_file)
        object = config.get(object)
    
    return object

def get_commit_message():
    # Get commit message
    """
    Prompt the user for a commit message and return the entered text.
    
    If the user provides an empty message, the process prints an error and exits with status 1.
    
    Returns:
        commit_message (str): The entered commit message with leading and trailing whitespace removed.
    """
    commit_message = input("Enter commit message: ").strip()

    if commit_message == "":
        print("Commit message cannot be empty.")
        sys.exit(1)
    
    return commit_message

def get_timestamp():
    """
    Return the current local timestamp in ISO 8601 format.
    
    Returns:
        timestamp (str): ISO 8601 formatted datetime string (e.g. '2026-05-04T12:34:56.123456').
    """
    return datetime.now().isoformat()

def get_current_branch():
   #Get current branch
    """
   Retrieve the name of the currently selected SCCS branch.
   
   Reads the `.sccs/current_branch/current_branch.json` file and returns the value of its `current_branch` key. Exits the process with status 1 if the current branch file is missing.
   
   Returns:
       str or None: The current branch name, or `None` if the `current_branch` key is absent.
   """
   current_branch_path = os.path.join(directory_path, ".sccs", "current_branch", "current_branch.json")
    if not Path(current_branch_path).is_file():
        print("Current branch file not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
        sys.exit(1)

    with open(current_branch_path, "r", encoding="utf-8", newline="\n") as current_branch_file:
        current_branch = json.load(current_branch_file).get("current_branch") 

    return current_branch

def get_history_path():
    """
    Builds the filesystem path to the commit history JSON for the current branch.
    
    Returns:
        str: Absolute path to the `commit_history.json` file for the current branch.
    """
    return os.path.join(directory_path, ".sccs", "branches", get_current_branch(), "history", "commit_history.json")

def get_commit_history():
    """
    Load and return the commit history JSON for the current branch.
    
    Exits the process with status 1 if the history file is missing or cannot be read or parsed.
    
    Returns:
        history (dict): The parsed JSON object representing commit history.
    """
    history_path = get_history_path()
    if not Path(history_path).is_file():
        print("History file not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
        sys.exit(1)

    try:
        with open(history_path, "r", encoding="utf-8", newline="\n") as history_file:
        
            history = json.load(history_file)

    except Exception as e:
        print(f"Error retrieving JSON from history file: {e}")
        sys.exit(1)

    return history

def get_parent_hash(history):
    """
    Return the latest commit hash recorded in the provided history structure.
    
    Parameters:
        history (dict): History object expected to contain a "history" mapping with a "latest_commit" key.
    
    Returns:
        str or None: The value of "latest_commit" if present, otherwise None.
    """
    parent_hash = history["history"].get("latest_commit")
    return parent_hash

def generate_commit_hash(timestamp, commit_message, name, email, parent_hash):
    """
    Compute a deterministic SHA-256 commit identifier from commit metadata.
    
    Parameters:
        timestamp (str): ISO8601 timestamp for the commit.
        commit_message (str): Commit message text.
        name (str): Author name.
        email (str): Author email.
        parent_hash (str): Parent commit hash (may be empty or None for initial commits).
    
    Returns:
        str: Hexadecimal SHA-256 digest representing the commit identifier.
    """
    return hashlib.sha256(f'{timestamp}/{commit_message}/{name}/{email}/{parent_hash}'.encode()).hexdigest()

def copy_docx_to_objects(sha_hash):
    """
    Copy the repository's current .docx file into the SCCS objects/docx directory using sha_hash as the filename while preserving file metadata.
    
    Parameters:
        sha_hash (str): SHA-256 hex digest used to name the copied object file (stored as "<sha_hash>.docx").
    """
    shutil.copy2(os.path.join(directory_path, Path(path).name) , os.path.join(directory_path, ".sccs", "objects", "docx", f"{sha_hash}.docx"))

def write_diff_html(sha_hash, docx_html):
    """
    Write the provided HTML (with CSS styles prepended) to the objects/html file named by the given SHA hash.
    
    Parameters:
        sha_hash (str): Hexadecimal identifier used as the output filename (written to .sccs/objects/html/<sha_hash>.html).
        docx_html (str): HTML content converted from the DOCX to be written into the file (styles are prepended).
    """
    with open(os.path.join(directory_path, ".sccs", "objects", "html", f"{sha_hash}.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(styles + docx_html)

def write_view_html(sha_hash, docx_html):
    """
    Write the DOCX-derived HTML wrapped for viewing to the objects/view_html directory using the commit hash as the filename.
    
    Parameters:
        sha_hash (str): Commit identifier used as the output filename (saved as "<sha_hash>.html").
        docx_html (str): HTML string produced from the DOCX conversion; passed through `wrap_html` before writing.
    """
    with open(os.path.join(directory_path, ".sccs", "objects", "view_html", f"{sha_hash}.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(wrap_html(docx_html))

def update_commit_log_history(history, sha_hash, timestamp, name, email, commit_message):
    # Update history
    """
    Update the repository commit history structure with a new commit entry and persist it to disk.
    
    This mutates the provided `history` mapping by:
    - setting `history["history"]["latest_commit"]` to the new commit hash,
    - incrementing `history["history"]["latest_commit_number"]` (defaults to 0) and recording the new hash under `history["history"]["commit_order"][<latest_commit_number>]`,
    - adding a new entry `history["log"][<sha_hash>]` containing `timestamp`, `author` formatted as "<name> <email>", and `message`;
    then writes the updated `history` as JSON to the path returned by `get_history_path()`.
    
    Parameters:
        history (dict): In-memory history object expected to contain at least the "history" and "log" mappings; will be modified in-place.
        sha_hash (str): Commit identifier to record.
        timestamp (str): ISO-formatted timestamp associated with the commit.
        name (str): Author name used to compose the `author` field.
        email (str): Author email used to compose the `author` field.
        commit_message (str): Commit message to store in the log entry.
    """
    history["history"]["latest_commit"] = f"{sha_hash}"
    history["history"]["latest_commit_number"] = history["history"].get("latest_commit_number", 0) + 1
    history["history"]["commit_order"][str(history["history"]["latest_commit_number"])] = f"{sha_hash}"

    history["log"][f"{sha_hash}"] = {
        "timestamp": timestamp,
        "author": f"{name} <{email}>",
        "message": commit_message
    }

    with open(get_history_path(), "w", encoding="utf-8", newline="\n") as history_file:
        json.dump(history, history_file, indent=4)

def update_commit_messages(sha_hash, commit_message):
    # Update commit messages
    """
    Record or update the commit message associated with a commit hash in the repository's commit_messages JSON.
    
    This writes the mapping sha_hash -> commit_message into
    <directory_path>/.sccs/commit_messages/commit_messages.json, persisting the updated JSON file.
    If the commit messages file does not exist, the function prints an initialization instruction and exits the process with status 1.
    
    Parameters:
        sha_hash (str): The commit identifier to associate the message with.
        commit_message (str): The commit message to store for the given hash.
    """
    commit_messages_path = os.path.join(directory_path, ".sccs", "commit_messages", "commit_messages.json")
    if not Path(commit_messages_path).is_file():
        print("Commit messages file not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
        sys.exit(1)

    with open(commit_messages_path, "r", encoding="utf-8", newline="\n") as commit_messages_file:
        messages = json.load(commit_messages_file)

    messages[f"{sha_hash}"] = f"{commit_message}"

    with open(commit_messages_path, "w", encoding="utf-8", newline="\n") as commit_messages_file:
        json.dump(messages, commit_messages_file, indent=4)

def update_commit_binary_hash_history(sha_hash, hash_docx_binary):
    # Update commit file hash
    """
    Record the binary hash of the DOCX for a commit in the branch's commit_file_hash JSON.
    
    Updates the branch-specific commit_file_hash.json by setting the key `sha_hash` to `hash_docx_binary` and writing the file back to disk. If the commit_file_hash file is missing or cannot be parsed, the function prints an initialization instruction and exits the process.
    
    Parameters:
        sha_hash (str): Commit identifier to use as the JSON key.
        hash_docx_binary (str): SHA-256 hex digest of the DOCX binary to store.
    """
    commit_file_hash_path = os.path.join(directory_path, ".sccs", "branches", get_current_branch(), "commit_file_hash", "commit_file_hash.json")
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

def print_confirmation_message(sha_hash):
    """
    Prints a confirmation message stating that a commit was created for the given commit hash.
    
    Parameters:
        sha_hash (str): The commit's SHA-256 hex digest to include in the message.
    """
    print(f"Commit {sha_hash} created successfully.")

hash_docx_binary = hash_current_docx_binary()

name = get_obj_from_config("name")

email = get_obj_from_config("email")

docx_html = convert_docx_to_html()

commit_message = get_commit_message()

timestamp = get_timestamp()

current_branch = get_current_branch()

history = get_commit_history()

parent_hash = get_parent_hash(history)

sha_hash = generate_commit_hash(timestamp, commit_message, name, email, parent_hash)

copy_docx_to_objects(sha_hash)

write_diff_html(sha_hash, docx_html)

write_view_html(sha_hash, docx_html)

update_commit_log_history(history, sha_hash, timestamp, name, email, commit_message)

update_commit_messages(sha_hash, commit_message)

update_commit_binary_hash_history(sha_hash, hash_docx_binary)

print_confirmation_message(sha_hash)