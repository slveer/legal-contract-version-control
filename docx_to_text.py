import subprocess
from pathlib import Path
import sys
import docx2txt 
import hashlib
from datetime import datetime

path = sys.argv[2] if len(sys.argv) > 1 else None



if Path("/Users/danielphillion/Documents/Cher-Père-Noël/.sccs").is_dir(): #f"{path.strip('.docx')}/.sccs"
    print("This file has already been initialized with SCCS")
    sys.exit(1)

elif path and path.endswith(".docx") and Path(path).is_file():
    docx_to_txt = docx2txt.process(path)
else: 
    print("Invalid file path, make sure the file exists and is a .docx file")
    sys.exit(1)

sha_hash = hashlib.sha256(f'{datetime.now().isoformat()}/initial_version'.encode()).hexdigest()

subprocess.run(["mkdir", "-p", path.strip(".docx")])
subprocess.run(["mv", path, path.strip(".docx")])
subprocess.run(["mkdir", "-p", f"{path.strip('.docx')}/.sccs"])
subprocess.run(["mkdir", "-p", f"{path.strip('.docx')}/.sccs/commits"])
subprocess.run(["mkdir", "-p", f"{path.strip('.docx')}/.sccs/history"])
subprocess.run(["mkdir", "-p", f"{path.strip('.docx')}/.sccs/commit_messages"])

with open(f"{path.strip('.docx')}/.sccs/commits/{sha_hash}.txt", "w") as f:
    f.write(docx_to_txt)

history_data = f"""
{{
    "initial commit": "{sha_hash}.txt"
}}
"""

with open(f"{path.strip('.docx')}/.sccs/history/commit_history.json", "w") as f:
    f.write(history_data)

commit_message_data = f"""
{{
    "{sha_hash}.txt": "initial commit (This is a default commit message for initial version)"
}}
"""

with open(f"{path.strip('.docx')}/.sccs/commit_messages/commit_messages.json", "w") as f:
    f.write(commit_message_data)