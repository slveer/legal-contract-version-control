import json
from pathlib import Path
import os
import sys

path = sys.argv[2] if len(sys.argv) > 2 else None

if path: 

    directory_path = Path(path).with_suffix("")

    # if directory basename = parent directory name (eg: user/file/file), use parent directory (eg: user/file).
    if directory_path.name == directory_path.parent.name:
        directory_path = directory_path.parent

    # Set path correctly, whether it was correct in the first place or not
    path = os.path.join(directory_path, os.path.basename(path))

    if not Path(path).is_file():
        print("File not found. Please provide a valid file path.")
        sys.exit(1)
else:
    print("No file path provided")
    sys.exit(1)

if not Path(os.path.join(directory_path, ".sccs")).is_dir():
    print("This file has not been initialized with SCCS.")
    print("Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

elif not path and Path(path).suffix.lower() == ".docx" and Path(path).is_file():
    print("Invalid file path, make sure the file exists and is a .docx file")
    sys.exit(1)
    