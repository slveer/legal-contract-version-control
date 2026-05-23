import os
import shutil
import sys
from pathlib import Path

from sccs_layout_check import path

from sccs_layout_check import check_sccs

check_sccs()

def get_commit_path_input():
    commit_path = input("Enter the path to the commit file (.docx): ").strip()
    return commit_path

def check_commit_path_input():
    commit_path = get_commit_path_input()
    if commit_path == "":
        print("Commit file path cannot be empty.")
        sys.exit(1)

    if not Path(commit_path).is_file() or Path(commit_path).suffix.lower() != ".docx":
        print("Invalid commit file path, make sure the file exists and is a .docx file")
        sys.exit(1)
    return commit_path

def confirm_before_proceeding():
    confirm = input(f"Are you sure you want to overwrite '{os.path.basename(path)}' with the contents of '{os.path.basename(commit_path)}'?\nThis action will replace the current content of the .docx file. (Y/N): ").strip().lower()
    if confirm != 'y':
        print("Update canceled.")
        sys.exit(0)

def check_changes():
    if Path(path).exists() and Path(commit_path).exists() and os.path.samefile(path, commit_path):
        print("The commit file is the same as the current file. No changes will be made.")
        sys.exit(0)

def open_file_commit():
    shutil.copy2(commit_path, path)

def print_confirmation_message():
    print(f"File '{os.path.basename(path)}' has been updated with the contents of '{os.path.basename(commit_path)}'.")

commit_path = get_commit_path_input()

check_commit_path_input()

confirm_before_proceeding()

check_changes()

open_file_commit()

print_confirmation_message()