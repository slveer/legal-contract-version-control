from sccs_layout_check import check_sccs, directory_path, sanitize_dirname
import sys
import os
import json
import shutil
check_sccs()

branch_to_switch = sys.argv[2] if len(sys.argv) > 2 else None

if branch_to_switch:
    branch_to_switch = sanitize_dirname(branch_to_switch)

if not branch_to_switch:
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

latest_commit_on_branch = commit_history["history"]["commit_order"][f"{commit_history['history']['latest_commit_number']}"]

if not os.path.isfile(os.path.join(directory_path, ".sccs", "objects", "docx", f"{latest_commit_on_branch}.docx")):
    print(f"Error: Commit object '{latest_commit_on_branch}' not found.")
    sys.exit(1)
try:
    shutil.copy2(os.path.join(directory_path, ".sccs", "objects", "docx", f"{latest_commit_on_branch}.docx"), os.path.join(directory_path, f"{os.path.basename(directory_path)}.docx"))
except Exception as e:
    print(f"Error switching to branch '{branch_to_switch}': {e}")
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