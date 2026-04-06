import os

from docx import Document
import sys
from pathlib import Path

# Get user inputted path argument
path = sys.argv[2] if len(sys.argv) > 2 else None

# Check if the path is provided
if path: 

    directory_path = Path(path).with_suffix("")

    # if directory basename = parent directory name (eg: user/file/file), use parent directory (eg: user/file).
    if directory_path.name == directory_path.parent.name:
        directory_path = directory_path.parent

    # Set path correctly, whether it was correct in the first place or not
    path = os.path.join(directory_path, os.path.basename(path))

    if not Path(path).is_file():
        print("Invalid file path, make sure the file exists and is a .docx file")
        sys.exit(1)
else:
    print("No file path provided")
    sys.exit(1)

# Check if the path ends with .docx and exists
if not Path(path).is_file() or Path(path).suffix.lower() != ".docx":
    print("Invalid file path, make sure the file exists and is a .docx file")
    sys.exit(1)

# Get user inputted commit path
commit_path = input("Enter the path to the commit file (.txt): ")

if not Path(commit_path).is_file() or Path(commit_path).suffix.lower() != ".txt":
    print("Invalid commit file path, make sure the file exists and is a .txt file")
    sys.exit(1)

with open(commit_path, 'r') as file:
    commit = file.read()
document = Document()
document.add_paragraph(commit)

confirm = input(f"Are you sure you want to overwrite '{os.path.basename(path)}' with the contents of '{os.path.basename(commit_path)}'?\nThis action will replace the current content of the .docx file. (Y/N): ").strip().lower()
if confirm != 'y':
    print("Update canceled.")
    sys.exit(0)

document.save(path)

print(f"File '{os.path.basename(path)}' has been updated with the contents of '{os.path.basename(commit_path)}'.")