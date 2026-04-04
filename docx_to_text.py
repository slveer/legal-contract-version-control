import subprocess
from pathlib import Path
import sys
import docx2txt 
import hashlib
from datetime import datetime

path = sys.argv[2] if len(sys.argv) > 1 else None
directory_path = f"{path.strip('.docx')}"

if Path(f"{directory_path}/.sccs").is_dir():
    print("This file has already been initialized with SCCS")
    sys.exit(1)

elif path and path.endswith(".docx") and Path(path).is_file():
    docx_to_txt = docx2txt.process(path)
else: 
    print("Invalid file path, make sure the file exists and is a .docx file")
    sys.exit(1)

name = input("Enter your name: ")
email = input("Enter your email: ")

sha_hash = hashlib.sha256(f'{datetime.now().isoformat()}/initial_version'.encode()).hexdigest()

subprocess.run(["mkdir", "-p", directory_path])
subprocess.run(["mv", path, directory_path])
subprocess.run(["mkdir", "-p", f"{directory_path}/.sccs"])
subprocess.run(["mkdir", "-p", f"{directory_path}/.sccs/commits"])
subprocess.run(["mkdir", "-p", f"{directory_path}/.sccs/history"])
subprocess.run(["mkdir", "-p", f"{directory_path}/.sccs/commit_messages"])
subprocess.run(["mkdir", "-p", f"{directory_path}/.sccs/config"])

with open(f"{directory_path}/.sccs/commits/{sha_hash}.txt", "w") as f:
    f.write(docx_to_txt)

history_data = f"""
{{
    "initial commit": "{sha_hash}.txt"
}}
"""

with open(f"{directory_path}/.sccs/history/commit_history.json", "w") as f:
    f.write(history_data)

commit_message_data = f"""
{{
    "{sha_hash}.txt": "initial commit (This is a default commit message for initial version)"
}}
"""

with open(f"{directory_path}/.sccs/commit_messages/commit_messages.json", "w") as f:
    f.write(commit_message_data)

config_data = f"""
{{
    "name": "{name}",
    "email": "{email}"
}}
"""

with open(f"{directory_path}/.sccs/config/config.json", "w") as f:
    f.write(config_data)