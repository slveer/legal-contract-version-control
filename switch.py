from sccs_layout_check import check_sccs, directory_path, sanitize_dirname, path
import hashlib
import sys
import os
import json
import shutil
check_sccs()

branch_to_switch = sys.argv[2] if len(sys.argv) > 2 else None

if branch_to_switch:
    branch_to_switch = sanitize_dirname(branch_to_switch)

if not branch_to_switch or len(branch_to_switch) == 0:
    print("No branch specified. Please provide a branch name to switch to.")
    sys.exit(1)

try:
    with open(os.path.join(directory_path, ".sccs",  "branches", branch_to_switch, "history", "commit_history.json"), "r", encoding="utf-8", newline="\n") as f:
        try:
            commit_history = json.load(f)
            
        except Exception as e:
            print(f"Error parsing commit history for branch '{branch_to_switch}': {e}")
            sys.exit(1)

except Exception as e: 
    print(f"Error reading commit history for branch '{branch_to_switch}': {e}")
    sys.exit(1)

try:
    latest_commit_on_branch = commit_history["history"]["latest_commit"]

except KeyError as e:
    print(f"Error: Missing key {e} in commit history for branch '{branch_to_switch}'.")
    sys.exit(1)

if not os.path.isfile(os.path.join(directory_path, ".sccs", "objects", "docx", f"{latest_commit_on_branch}.docx")):
    print(f"Error: Commit object '{latest_commit_on_branch}' not found.")
    sys.exit(1)

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
    with open(os.path.join(directory_path, ".sccs", "current_branch", "current_branch.json"), "r", encoding="utf-8", newline="\n") as f:
        try:
            current_branch = json.load(f)
        except Exception as e:
            print(f"Error reading current branch information: {e}")
            sys.exit(1)
except Exception as e:
    print(f"Error accessing current branch information: {e}")
    sys.exit(1)

try:
    with open(os.path.join(directory_path, ".sccs", "branches", current_branch["current_branch"], "commit_file_hash", "commit_file_hash.json"), "r", encoding="utf-8", newline="\n") as f:
        try:
            commit_file_hash = json.load(f).get(latest_commit_on_branch)
        except Exception as e:    
            print(f"Error reading commit file hash information: {e}")
            sys.exit(1)
except Exception as e:
    print(f"Error accessing commit file hash information: {e}")
    sys.exit(1)

if not commit_file_hash == hashed_file:
    print(f"Error: Cannot switch to branch '{branch_to_switch}' because the current file has uncommitted changes, or the byte content does not match the latest commit. Please commit your changes before switching branches.
          ")
    sys.exit(1)

try:
    shutil.copy2(os.path.join(directory_path, ".sccs", "objects", "docx", f"{latest_commit_on_branch}.docx"), os.path.join(directory_path, f"{os.path.basename(directory_path)}.docx"))
except Exception as e:
    print(f"Error switching to branch '{branch_to_switch}': {e}")
    sys.exit(1)



current_branch["current_branch"] = branch_to_switch

try:
    with open(os.path.join(directory_path, ".sccs", "current_branch", "current_branch.json"), "w", encoding="utf-8", newline="\n") as f:
        try:
            json.dump(current_branch, f, indent=4)
        except Exception as e:
            print(f"Error writing current branch information: {e}")
            sys.exit(1)
except Exception as e:
    print(f"Error updating current branch information: {e}")
    sys.exit(1)

print(f"Successfully switched to branch '{branch_to_switch}'.")