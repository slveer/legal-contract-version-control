import os
import shutil
import sys
from pathlib import Path

# # Get user inputted path argument
# path = sys.argv[2] if len(sys.argv) > 2 else None

# # Check if the path is provided
# if path: 

#     directory_path = Path(path).with_suffix("")

#     # if directory basename = parent directory name (eg: user/file/file), use parent directory (eg: user/file).
#     if directory_path.name == directory_path.parent.name:
#         directory_path = directory_path.parent

#     # Set path correctly, whether it was correct in the first place or not
#     path = os.path.join(directory_path, os.path.basename(path))

#     if not Path(path).is_file():
#         print("Invalid file path, make sure the file exists and is a .docx file")
#         sys.exit(1)
# else:
#     print("No file path provided")
#     sys.exit(1)

# # Check if the directory contains an SCCS initialization
# if not Path(os.path.join(directory_path, ".sccs")).is_dir():
#     print("This file has not been initialized with SCCS.")
#     print("Please run 'sccs init <file_path>' to initialize SCCS for this file.")
#     sys.exit(1)
    
# # Check if the path ends with .docx and exists
# if not Path(path).is_file() or Path(path).suffix.lower() != ".docx":
#     print("Invalid file path, make sure the file exists and is a .docx file")
#     sys.exit(1)

directory_path = os.getcwd()

path = os.path.join(directory_path, f"{os.path.basename(directory_path)}.docx")

sccs_dir = os.path.join(directory_path, ".sccs")

if not Path(sccs_dir).is_dir():
    print("This file has not been initialized with SCCS.")
    print("Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(os.path.join(sccs_dir, "commit_file_hash")).is_dir():
    print("Commit file hash directory not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(os.path.join(sccs_dir, "commit_file_hash.json")).is_file():
    print("Commit file hash JSON not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(os.path.join(sccs_dir, "commit_messages")).is_dir():
    print("Commit messages directory not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(os.path.join(sccs_dir, "commit_messages.json")).is_file():
    print("Commit messages JSON not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(os.path.join(sccs_dir, "commits")).is_dir():
    print("Commits directory not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(os.path.join(sccs_dir, "commits", "txt-commits")).is_dir():
    print("Text commits directory not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(os.path.join(sccs_dir, "commits", "docx-commits")).is_dir():
    print("Docx commits directory not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(os.path.join(sccs_dir, "config")).is_dir():
    print("Config directory not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(os.path.join(sccs_dir, "config", "config.json")).is_file():
    print("Config file not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(os.path.join(sccs_dir, "history")).is_dir():
    print("History directory not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(os.path.join(sccs_dir, "history", "commit_history.json")).is_file():
    print("History file not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(os.path.join(sccs_dir, "history", "commit_history.json")).is_file():
    print("History file not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(path).is_file():
    print("Docx file not found. Re-initialize SCCS for this file with 'sccs init <file_path>'")
    sys.exit(1)

# Get user inputted commit path
commit_path = input("Enter the path to the commit file (.docx): ")

if not Path(commit_path).is_file() or Path(commit_path).suffix.lower() != ".docx":
    print("Invalid commit file path, make sure the file exists and is a .docx file")
    sys.exit(1)

confirm = input(f"Are you sure you want to overwrite '{os.path.basename(path)}' with the contents of '{os.path.basename(commit_path)}'?\nThis action will replace the current content of the .docx file. (Y/N): ").strip().lower()
if confirm != 'y':
    print("Update canceled.")
    sys.exit(0)

if Path(path).exists() and Path(commit_path).exists() and os.path.samefile(path, commit_path):
    print("The commit file is the same as the current file. No changes will be made.")
    sys.exit(0)

shutil.copy2(commit_path, path)

print(f"File '{os.path.basename(path)}' has been updated with the contents of '{os.path.basename(commit_path)}'.")