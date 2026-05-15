import re
import sys
import os
import json
import shutil
from sccs_layout_check import check_sccs, directory_path

def sanitize_dirname(name):
    return re.sub(r'[\\/:*?"<>|]', '-', name).strip('. ')

current_branch_path = os.path.join(directory_path, ".sccs", "current_branch", "current_branch.json")
try:
    with open(current_branch_path, "r", encoding="utf-8", newline="\n") as current_branch_file:
        try:
            branch_data = json.load(current_branch_file)
            current_branch = branch_data.get("current_branch")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from current branch file: {e}")
            sys.exit(1)

except Exception as e:
    print(f"Error reading current branch data: {e}")

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
    sanitized_branch_name = sanitize_dirname(branch_name)

    if not len(sanitized_branch_name) > 0:
        print("Invalid branch name. Please provide a valid branch name.")
        sys.exit(1)

    if sanitized_branch_name in branch_data["branches"]:
        print(f"Branch '{sanitized_branch_name}' already exists.")
        sys.exit(1)

    if os.path.isdir(os.path.join(directory_path, ".sccs", "branches", sanitized_branch_name)):
        print(f"Branch '{sanitized_branch_name}' already exists, or a directory with the same name exists.")
        sys.exit(1)
        
    if not os.path.isdir(os.path.join(directory_path, ".sccs", "branches", sanitized_branch_name)):
        shutil.copytree(os.path.join(directory_path, ".sccs", "branches", current_branch), os.path.join(directory_path, ".sccs", "branches", sanitized_branch_name))

        with open(current_branch_path, "w", encoding="utf-8", newline="\n") as current_branch_file:
            json.dump(branch_data, current_branch_file, indent=4)
            branch_data["branches"].append(sanitized_branch_name)

        print(f"Branch '{sanitized_branch_name}' was created from branch '{current_branch}'.")
         

if subcommand == 'delete':
    sanitized_branch_name = sanitize_dirname(branch_name)

    branch_path = os.path.join(directory_path, ".sccs", "branches", sanitized_branch_name)

    if sanitized_branch_name == current_branch:
        print("Cannot delete the current branch.")
        sys.exit(1)

    if not os.path.exists(branch_path):
        print(f"Branch '{sanitized_branch_name}' does not exist.")
        sys.exit(1)

    if not sanitized_branch_name in branch_data["branches"]:
        print(f"Branch '{sanitized_branch_name}' does not exist in branch data.")
        sys.exit(1)

    try:
        shutil.rmtree(branch_path, ignore_errors=True)

    except Exception as e:
        print(f"Error deleting branch '{sanitized_branch_name}': {e}")
        sys.exit(1)
    branch_data["branches"].remove(sanitized_branch_name)

    try:
        with open(current_branch_path, "w", encoding="utf-8", newline="\n") as current_branch_file:
            json.dump(branch_data, current_branch_file, indent=4)
        
    except Exception as e:
        print(f"Error updating branch data: {e}")
        sys.exit(1)
    
    print(f"Branch '{sanitized_branch_name}' was deleted.")

if subcommand == "list":
    print("Branches:")
    for branch in branch_data.get("branches", []):
        if branch == current_branch:
            print(f"* {branch} (current)")
        else:
            print(f"  {branch}")