import json
from pathlib import Path
import os
import sys

from sccs_layout_check import directory_path

from sccs_layout_check import path

from sccs_layout_check import check_sccs

check_sccs()

# Get JSON log data
log_path = os.path.join(directory_path, ".sccs", "history", "commit_log.json")
if not Path(log_path).is_file():
    print("Log file not found. Please make sure the file has been initialized with SCCS.")
    sys.exit(1)

with open(log_path, "r", encoding="utf-8", newline="\n") as log_file:
    log_data = json.load(log_file)
# Print log data
for entry in log_data:
    print(
        "------------------------------\n"
        f"Commit File: {entry}\n"
        f"Author: {log_data[entry]['author']}\n"
        f"Date: {log_data[entry]['timestamp']}\n"
        f"Message: {log_data[entry]['message']}\n"
        "-----------------------------"
    )