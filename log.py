import json
from pathlib import Path
import os
import sys

from sccs_layout_check import directory_path

from sccs_layout_check import check_sccs

CURRENT_BRANCH_PATH = os.path.join(directory_path, ".sccs", "current_branch", "current_branch.json")

check_sccs()

def get_current_branch():
    with open(CURRENT_BRANCH_PATH, "r", encoding="utf-8", newline="\n") as current_branch_file:
            current_branch = json.load(current_branch_file).get("current_branch")
    return current_branch

def get_log_data():
    # Get JSON log data
    log_path = os.path.join(directory_path, ".sccs", "branches", get_current_branch, "history", "commit_history.json")
    if not Path(log_path).is_file():
        print("Log file not found. Please make sure the file has been initialized with SCCS.")
        sys.exit(1)

    with open(log_path, "r", encoding="utf-8", newline="\n") as log_file:
        log_data = json.load(log_file)
    return log_data

def print_log():
   for entry in get_log_data()["log"]:
       print(
           "------------------------------\n"
           f"Commit File: {entry}\n"
           f"Author: {get_log_data()['log'][entry]['author']}\n"
           f"Date: {get_log_data()['log'][entry]['timestamp']}\n"
           f"Message: {get_log_data()['log'][entry]['message']}\n"
           "------------------------------"
       )