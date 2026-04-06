from docx import Document
import sys
from pathlib import Path

# Get user inputted path argument
path = sys.argv[2] if len(sys.argv) > 2 else None

# Check if the path is provided
if not path: 
    print("No file path provided")
    sys.exit(1)

# Check if the path ends with .docx and exists
if not Path(path).is_file() or Path(path).suffix.lower() != ".docx":
    print("Invalid file path, make sure the file exists and is a .docx file")
    sys.exit(1)

# Get user inputted commit path
commit_path = input("Enter the path to the commit file (.txt): ")

with open(commit_path, 'r') as file:
    commit = file.read()
document = Document(path)
document.add_paragraph(commit)
document.save(path)


