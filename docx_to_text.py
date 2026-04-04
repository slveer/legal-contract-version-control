import subprocess
from pathlib import Path
import sys
import docx2txt 

path = sys.argv[2] if len(sys.argv) > 1 else None

if path and path.endswith(".docx") and Path(path).is_file():
    docx_to_txt = docx2txt.process(path)
else: 
    print("Invalid file path, make sure the file exists and is a .docx file")
    sys.exit(1)

subprocess.run(["mkdir", "-p", path.strip(".docx")])
subprocess.run(["mv", path, path.strip(".docx")])
subprocess.run(["mkdir", "-p", f"{path.strip('.docx')}/.sccs"])

with open(f"{path.strip('.docx')}/.sccs/output.txt", "w") as f:
    f.write(docx_to_txt)

