from pathlib import Path
import random
import sys
import docx2txt 
import string

path = sys.argv[2] if len(sys.argv) > 1 else None

if Path(path).is_file():
    text = docx2txt.process(path)
else:
    print("Invalid file path")
    sys.exit(1)
    
file_hash = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))

with open(f"{file_hash}.txt", "w") as f:
    f.write(text)
