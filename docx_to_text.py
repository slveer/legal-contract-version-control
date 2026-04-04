from asyncio import subprocess
from pathlib import Path
import random
import sys
import docx2txt 
import string
import os

path = sys.argv[2] if len(sys.argv) > 1 else None
if '.docx' in path:
    text = docx2txt.process(path)

elif Path(path).is_file():
    text = docx2txt.process(path)

else:
    print("Invalid file path, make sure the file exists and is a .docx file")
    sys.exit(1)

subprocess.run(["unzip", f"{path}", "-d", path.strip(".docx")])

file_hash = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))

with open(f"{file_hash}.txt", "w") as f:
    f.write(text)


