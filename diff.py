import os
from pathlib import Path
from pydoc import html
import sys
from difflib import HtmlDiff
from bs4 import BeautifulSoup
import mammoth

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

if Path(commit_to_diff).suffix.lower() != ".html":
    print("Commit file is not a .html file. Please provide a valid .html commit file.")
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

with open(base_file, "rb") as f:
    base_html = mammoth.convert_to_html(f).value

with open(commit_to_diff, "r", encoding="utf-8", newline="\n") as commit_file:
    commit_html = commit_file.read()

commit = BeautifulSoup(commit_html, "html.parser")


current = BeautifulSoup(base_html, "html.parser")


d = HtmlDiff()



diff = d.make_file(
    current.prettify().splitlines(), 
    commit.prettify().splitlines(),
    fromdesc="Current", 
    todesc="Commit"
)
        

soup = BeautifulSoup(diff, "html.parser")

for tag in soup.find_all(attrs={"nowrap": True}):
    del tag["nowrap"]

style = soup.find("style")

style.string += "\ntd { word-wrap: break-word; max-width: 48vw; white-space: pre-wrap; }"

with open("diff.html", "w", encoding="utf-8") as f:
    f.write(str(soup))