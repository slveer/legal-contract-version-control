import os
from pathlib import Path
import sys
from difflib import unified_diff
import docx2txt

# base_file = sys.argv[2] if len(sys.argv) > 2 else None
commit_to_diff = sys.argv[2] if len(sys.argv) > 2 else None 

directory_path = os.getcwd()

base_file = os.path.join(directory_path, f"{os.path.basename(directory_path)}.docx")

sccs_dir = os.path.join(directory_path, ".sccs")

if not commit_to_diff:
    print("No commit file specified.")
    sys.exit(1)

if not Path(commit_to_diff).is_file():
    print("Commit file not found. Please provide a valid commit file path.")
    sys.exit(1)

if not Path(sccs_dir).is_dir():
    print("This file has not been initialized with SCCS.")
    print("Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(os.path.join(sccs_dir, "commit_file_hash")).is_dir():
    print("Commit file hash directory not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(os.path.join(sccs_dir, "commit_file_hash", "commit_file_hash.json")).is_file():
    print("Commit file hash JSON not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(os.path.join(sccs_dir, "commit_messages")).is_dir():
    print("Commit messages directory not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

if not Path(os.path.join(sccs_dir, "commit_messages", "commit_messages.json")).is_file():
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

if not Path(base_file).is_file():
    print("Docx file not found. Re-initialize SCCS for this file with 'sccs init <file_path>'")
    sys.exit(1)

try:
    with open(commit_to_diff, "r", encoding="utf-8", newline="\n") as commit_file:
        commit_text = commit_file.read()

except Exception as e:
    print(f"Error processing commit .txt file: {e}")       
    sys.exit(1)

try: 
    with open(base_file, "r", encoding="utf-8", newline="\n") as base_file_obj:
        base_text = base_file_obj.read()

except Exception as e:
    print(f"Error processing base .docx file: {e}")       
    sys.exit(1)

# Use difflib to compare the two texts and print the differences
def to_lines(text):
    return [line + "\n" for line in text.splitlines()]

diff = (
    unified_diff(
        to_lines(base_text),
        to_lines(commit_text),
        fromfile=Path(base_file).name, 
        tofile=Path(commit_to_diff).name
    )
)

first_diff_line = next(diff, None)

if first_diff_line is None:
    print("No differences found between the base file and the commit.")
    print("Diff complete.")
    sys.exit(0)

else:
    diff = [first_diff_line] + list(diff)
    print("".join(diff))

print("Diff complete.")

