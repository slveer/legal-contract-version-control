import os
import shutil
from pathlib import Path
import sys
import docx2txt 
import hashlib
from datetime import datetime
import json


# Get user inputted path argument
path = sys.argv[2] if len(sys.argv) > 2 else None

# Strip .docx extension from the file name to create a directory
if path: 
    directory_path = Path(path).with_suffix('')
else:
    print("No file path provided")
    sys.exit(1)

# Check if the directory contains an SCCS initialization
if not Path(os.path.join(directory_path, ".sccs")).is_dir():
    print("This file has not been initialized with SCCS.")
    print("Please run 'sccs init <file_path>' to initialize SCCS for this file.")
    sys.exit(1)

elif path and Path(path).suffix.lower() == ".docx" and Path(path).is_file():
    try: 
        commit = docx2txt.process(path)
    except Exception as e:
        print(f"Error processing .docx file: {e}")
        sys.exit(1)

# if not, exit  
else: 
    print("Invalid file path, make sure the file exists and is a .docx file")
    sys.exit(1)

