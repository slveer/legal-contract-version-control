import os
from pathlib import Path
from pydoc import html, text
import sys
from difflib import HtmlDiff
from bs4 import BeautifulSoup
import mammoth
import difflib
import re

def p_to_list(html: str) -> list:
    p = re.findall(r'<(?:h1|h2|h3|h4|h5|h6|p|li|blockquote|td|a) number="\d+">(.*?)</(?:h1|h2|h3|h4|h5|h6|p|li|blockquote|td|a)>', html)
    for i in range(len(p)):
        p[i] = re.sub(r'<[^>]+>', '', p[i])
    return p

def replace_p(html, strings_old, strings_new: str) -> str:
    result = html
    for i in range(min(len(strings_old), len(strings_new))):
        result = result.replace(strings_old[i], f"{strings_old[i]}||{strings_new[i]}")
    
    for i in range(len(strings_new), len(strings_old)):
        result = result.replace(strings_old[i], f"{strings_old[i]}||''")
    
    return result

def delete_p(html, strings_old: str) -> str:
    result = html
    for s in strings_old:
        result = result.replace(s, f"{s}||''")
    return result

def strip_tags(html: str) -> str:
    counter = 0
    def replace_tag(match):
        nonlocal counter
        tag = match.group(1)
        inner = re.sub(r'<[^>]+>', '', match.group(2))
        result = f'<{tag} number="{counter}">{inner}</{tag}>'
        counter += 1
        return result
    return re.sub(r"<(h1|h2|h3|h4|h5|h6|p|li|blockquote|td|a)>(.*?)</\1>", replace_tag, html, flags=re.DOTALL)

# base_file = sys.argv[2] if len(sys.argv) > 2 else None
commit_to_diff = sys.argv[2] if len(sys.argv) > 2 else None 

directory_path = os.getcwd()

docx_current_version = os.path.join(directory_path, f"{os.path.basename(directory_path)}.docx")

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

if not Path(docx_current_version).is_file():
    print("Docx file not found. Re-initialize SCCS for this file with 'sccs init <file_path>'")
    sys.exit(1)

with open(docx_current_version, "rb") as f:
    docx_current_version_html = mammoth.convert_to_html(f).value

with open(commit_to_diff, "r", encoding="utf-8", newline="\n") as f:
    commit_html = f.read()

formatted_commit = BeautifulSoup(commit_html, "html.parser")

formatted_docx_current_version = BeautifulSoup(docx_current_version_html, "html.parser")
    


striped_tags_commit = strip_tags(str(formatted_commit))

strip_tags_docx_current_version = strip_tags(str(formatted_docx_current_version))


p_in_commit = p_to_list(striped_tags_commit)

p_in_docx_current_version = p_to_list(strip_tags_docx_current_version)

diff = difflib.SequenceMatcher(None, p_in_commit, p_in_docx_current_version)

diff_opcodes = diff.get_opcodes()

redline = striped_tags_commit

for opcode in diff_opcodes:
    tag, i1, i2, j1, j2 = opcode
    old = p_in_commit[i1:i2]
    new = p_in_docx_current_version[j1:j2]
    substring_old = p_in_commit[i1:i2]
    substring_new = p_in_docx_current_version[j1:j2]
    print(opcode)

    if tag == "replace":
        redline = replace_p(redline, substring_old, substring_new)

    if tag == "delete":
        redline = delete_p(redline, substring_old)

with open("redline_diff.html", "w", encoding="utf-8") as f:
    f.write(redline)