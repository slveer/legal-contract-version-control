import os
from pathlib import Path
import sys
from bs4 import BeautifulSoup
import mammoth
import difflib
import re

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

def strip_tags(html: str) -> str:
    counter = 0
    def replace_tag(match):
        nonlocal counter
        tag = match.group(1)
        inner = re.sub(r'<[^>]+>', '', match.group(2))
        result = f'<{tag} number="{counter}">{inner}</{tag}>'
        counter += 1
        return result
    return re.sub(r"<(h1|h2|h3|h4|h5|h6|p|li|blockquote|a)>(.*?)</\1>", replace_tag, html, flags=re.DOTALL)

def html_el_to_list(html: str) -> list:
    text = re.findall(r'<(?:h1|h2|h3|h4|h5|h6|p|li|blockquote|a) number="\d+">(.*?)</(?:h1|h2|h3|h4|h5|h6|p|li|blockquote|a)>', html)
    for i in range(len(text)):
        text[i] = re.sub(r'<[^>]+>', '', text[i])
    return text

def html_el_to_tag_and_number(html: str) -> list:
    result = html
    text = re.findall(r'<(h1|h2|h3|h4|h5|h6|p|li|blockquote|a) number="(\d+)">', result)
    return text

def replace_tag(html, old_strings, new_strings) -> str:
    result = html
    for i in range(min(len(old_strings), len(new_strings))):
        result = re.sub(rf'<(h1|h2|h3|h4|h5|h6|p|li|blockquote|a) number="{i}">{old_strings[i]}</\1>', rf'<\1 number="{i}"><span class=\"removed\">{old_strings[i]}</span> <span class=\"added\">{new_strings[i]}</span></\1>', result)

    for i in range(len(new_strings), len(old_strings)):
        result = re.sub(rf'<(h1|h2|h3|h4|h5|h6|p|li|blockquote|a) number="{i1}">{old_strings[i]}</\1>', rf'<(h1|h2|h3|h4|h5|h6|p|li|blockquote|a) number="{i1}"><span class=\"removed\">{old_strings[i]}</span></\1>', result)
        
    return result

def delete_tag(html, old_strings) -> str:
    result = html
    for item in old_strings:
        result = result.replace(item, f"<span class=\"removed\">{item}</span>")
    return result

def insert_tag(html, new_strings, i1, current_docx_striped_tags) -> str:
    first_changed_tag = i1
    result = html
    tags = html_el_to_tag_and_number(current_docx_striped_tags)
    def replace_callback(match):
        nonlocal first_changed_tag
        matched = match.group(0)
        matched = matched.replace(f"number={i1}", f"number=new")
        added_tags = []
        if i1 > 0:
            for i in new_strings:
                added_tags.append(f'<{tags[first_changed_tag][0]}><span class=\"added\">{i}</span></{tags[first_changed_tag][0]}>')
                first_changed_tag += 1
            return f"{matched}{''.join(added_tags)}"
        else:
            return f"{''.join(added_tags)}{matched}"
    if i1 > 0:
        result = re.sub(rf'<(h1|h2|h3|h4|h5|h6|p|li|blockquote|a) number="{i1 - 1}"(.*?)>(.*?)</\1>', replace_callback, html, flags=re.DOTALL)
    else:
        result = re.sub(rf'<(h1|h2|h3|h4|h5|h6|p|li|blockquote|a) number="{i1}"(.*?)>(.*?)</\1>', replace_callback, html, flags=re.DOTALL)
    return result

with open(docx_current_version, "rb") as f:
    docx_current_version_html = mammoth.convert_to_html(f).value

with open(commit_to_diff, "r", encoding="utf-8", newline="\n") as f:
    commit_html = f.read()

striped_tags_commit = strip_tags(str(BeautifulSoup(commit_html, "html.parser")))

strip_tags_docx_current_version = strip_tags(str(BeautifulSoup(docx_current_version_html, "html.parser")))

p_in_commit = html_el_to_list(striped_tags_commit)

p_in_docx_current_version = html_el_to_list(strip_tags_docx_current_version)

diff = difflib.SequenceMatcher(None, p_in_commit, p_in_docx_current_version)

diff_opcodes = diff.get_opcodes()

redline = striped_tags_commit

for opcode in diff_opcodes:
    tag, i1, i2, j1, j2 = opcode
    old = p_in_commit[i1:i2]
    new = p_in_docx_current_version[j1:j2]
    substring_old = p_in_commit[i1:i2]
    substring_new = p_in_docx_current_version[j1:j2]

    if tag == "replace":
        redline = replace_tag(redline, substring_old, substring_new)

    if tag == "delete":
        redline = delete_tag(redline, substring_old)

    if tag == "insert":
        redline = insert_tag(redline, substring_new, i1, strip_tags_docx_current_version)

with open("redline_diff.html", "w", encoding="utf-8") as f:
    f.write(redline)
