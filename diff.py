import os
from pathlib import Path
import sys
from bs4 import BeautifulSoup
import mammoth
import difflib
import re
from html import escape
from sccs_layout_check import check_sccs

check_sccs()

# base_file = sys.argv[2] if len(sys.argv) > 2 else None
commit_to_diff = sys.argv[2] if len(sys.argv) > 2 else None 

directory_path = os.getcwd()

docx_current_version = os.path.join(directory_path, f"{os.path.basename(directory_path)}.docx")

if not commit_to_diff:
    print("No commit file specified.")
    sys.exit(1)

if not Path(commit_to_diff).is_file():
    print("Commit file not found. Please provide a valid commit file path.")
    sys.exit(1)

if Path(commit_to_diff).suffix.lower() != ".html":
    print("Commit file is not a .html file. Please provide a valid .html commit file.")
    sys.exit(1)

if not Path(docx_current_version).is_file():
    print("Docx file not found. Re-initialize SCCS for this file with 'sccs init <file_path>'")
    sys.exit(1)

with open(docx_current_version, "rb") as f:
    try:
        docx_current_version_html = mammoth.convert_to_html(f).value

    except Exception as e:
        print(f"Error converting .docx to HTML: {e}")
        sys.exit(1)

with open(commit_to_diff, "r", encoding="utf-8", newline="\n") as f:
    commit_html = f.read()

def remove_inline_semantics(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all():
        if tag.name in ["b", "i", "u", "strong", "em"]:
            tag.unwrap()
    return str(soup)

def number_tags(html):
    soup = BeautifulSoup(html, "html.parser")
    for i, tag in enumerate(soup.find_all()):
        tag['data-number'] = str(i)
    return str(soup)

def tags_to_list(html):
    soup = BeautifulSoup(html, "html.parser")
    return [str(tag) for tag in soup.find_all()]
