import os
from pathlib import Path
import sys

import docx2txt

base_file = sys.argv[2] if len(sys.argv) > 2 else None
commit_to_diff = sys.argv[3] if len(sys.argv) > 3 else None

if base_file or commit_to_diff:
    
    directory_path = Path(base_file).with_suffix('')
    if directory_path.name == directory_path.parent.name:
        directory_path = directory_path.parent
    
    base_file = os.path.join(directory_path, os.path.basename(base_file))

    if not Path(base_file).is_file():
        print("Base file not found. Please provide a valid base file path.")
        sys.exit(1)
else:
    print("Please provide both the base file path and the commit hash to compare.")
    sys.exit(1)

if not Path(os.path.join(directory_path, ".sccs")).is_dir():
    print("This file has not been initialized with SCCS.")
    print("Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

elif base_file and Path(base_file).suffix.lower() == ".docx" and Path(base_file).is_file():
    try: 
        base_text = docx2txt.process(base_file)
    except Exception as e:
        print(f"Error processing base .docx file: {e}")
        sys.exit(1)

else: 
    print("Invalid base file path, make sure the file exists and is a .docx file")
    sys.exit(1)

if not commit_to_diff:
    print("No commit hash provided to compare.")
    sys.exit(1)

elif not Path(commit_to_diff).suffix.lower() == ".txt" or not Path(commit_to_diff).is_file():
    print("Invalid commit file path, make sure the file exists and is a .txt file")
    sys.exit(1)
else:
    try:
        with open(commit_to_diff, "r", encoding="utf-8", newline="\n") as commit_file:
            commit_text = commit_file.read()
    except Exception as e:
        print(f"Error processing commit .txt file: {e}")
        sys.exit(1)




