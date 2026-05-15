import sys
import os
import json
import shutil
from sccs_layout_check import check_sccs, directory_path

current_branch_path = os.path.join(directory_path, ".sccs", "current_branch.json")
with open(current_branch_path, "r", encoding="utf-8", newline="\n") as current_branch_file:
    current_branch = json.load(current_branch_file).get("current_branch")

check_sccs()

subcommand = sys.argv[2] if len(sys.argv) > 2 else None

branch_name = sys.argv[3] if len(sys.argv) > 3 else None

if not subcommand:
    print("No subcommand provided. Please use 'create', 'delete', or 'list' along with required arguments.")
    sys.exit(1)

if subcommand not in ["create", "delete", "list"]:
    print(f"Unknown subcommand: {subcommand}")
    print("Invalid subcommand. Please use 'create', 'delete', or 'list' along with required arguments.")
    sys.exit(1)

if subcommand in ["create", "delete"]:
    if not branch_name:
        print("No branch name provided. Please specify a branch name.")
        sys.exit(1)

if subcommand == 'create':
    shutil.copy2(os.path.join(directory_path, ".sccs", "branches", current_branch), os.path.join(directory_path, ".sccs", "branches", branch_name))
    with open(current_branch_path, "w", encoding="utf-8", newline="\n") as current_branch_file:
        json.dump({"current_branch": branch_name}, current_branch_file)
    print(f"Branch '{branch_name}' was created and set as the current branch.")