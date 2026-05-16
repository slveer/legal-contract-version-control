from sccs_layout_check import check_sccs, directory_path, path
import sys
import os
import json
check_sccs()

branch_to_switch = sys.argv[2] if len(sys.argv) > 2 else None

if not branch_to_switch:
    print("No branch specified. Please provide a branch name to switch to.")
    sys.exit(1)

try:
    with open(os.path.join(directory_path, ".sccs",  "branches", branch_to_switch, "history", "commit_history.json"), "r") as f:
        try:
            commit_history = json.load(f)
            
        except Exception as e:
            print(f"Error parsing commit history for branch '{branch_to_switch}': {e}")
            sys.exit(1)

except Exception as e: 
    print(f"Error reading commit history for branch '{branch_to_switch}': {e}")
    sys.exit(1)

latest_commit_on_branch = commit_history["history"]["commit_order"][f"{commit_history['history']['latest_commit_number']}"]