import os
from pathlib import Path
import sys
from bs4 import BeautifulSoup
import mammoth
import difflib
import re

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

def strip_tags(html: str) -> str:
    counter = 0
    def add_number_attribute(match):
        nonlocal counter
        tag = match.group(1)
        inner = re.sub(r'<[^>]+>', '', match.group(2))
        result = f'<{tag} number="{counter}">{inner}</{tag}>'
        counter += 1
        return result
    return re.sub(r"<(h1|h2|h3|h4|h5|h6|p|li|blockquote|a)\b[^>]*>(.*?)</\1>", add_number_attribute, html, flags=re.DOTALL)

def html_el_to_list(html: str) -> list:
    text = re.findall(r'<(?:h1|h2|h3|h4|h5|h6|p|li|blockquote|a) number="\d+">(.*?)</(?:h1|h2|h3|h4|h5|h6|p|li|blockquote|a)>', html)
    for i in range(len(text)):
        text[i] = re.sub(r'<[^>]+>', '', text[i])
    return text

def html_el_to_tag_and_number(html: str) -> list:
    result = html
    text = re.findall(r'<(h1|h2|h3|h4|h5|h6|p|li|blockquote|a) number="(\d+)">', result)
    return text

def replace_tag(html, old_strings, new_strings, i1) -> str:
    result = html
    for i in range(min(len(old_strings), len(new_strings))):
        result = re.sub(rf'<(h1|h2|h3|h4|h5|h6|p|li|blockquote|a) number="{i}">{re.escape(old_strings[i])}</\1>', rf'<\1 number="{i}"><span class=\"removed\">{re.escape(old_strings[i])}</span> <span class=\"added\">{re.escape(new_strings[i])}</span></\1>', result)

    for i in range(len(new_strings), len(old_strings)):
        result = re.sub(rf'<(h1|h2|h3|h4|h5|h6|p|li|blockquote|a) number="{i1}">{re.escape(old_strings[i])}</\1>', rf'<(h1|h2|h3|h4|h5|h6|p|li|blockquote|a) number="{i1}"><span class=\"removed\">{re.escape(old_strings[i])}</span></\1>', result)
        
    return result

def delete_tag(html, old_strings, i1, i2) -> str:
    result = html
    for i in range(i1, i2):
        for item in old_strings:
            re.sub(rf"<(h1|h2|h3|h4|h5|h6|p|li|blockquote|a) number=\"{i}\">{re.escape(item)}</\1>", f"<span class=\"removed\">{html.escape(item)}</span>", result)
    return result

def insert_tag(html, new_strings, i1, current_docx_stripped_tags) -> str:
    first_changed_tag = i1
    result = html
    tags = html_el_to_tag_and_number(current_docx_stripped_tags)
    def replace_callback(match):
        nonlocal first_changed_tag
        matched = match.group(0)
        matched = re.sub(rf'number="\d+"', f'number="new"', matched, count=1)
        added_tags = []
        for i in new_strings:
            added_tags.append(f'<{tags[first_changed_tag][0]}><span class=\"added\">{html.escape(i)}</span></{tags[first_changed_tag][0]}>')
            first_changed_tag += 1
        if i1 > 0:
            return f"{matched}{''.join(added_tags)}"
        else:
            return f"{''.join(added_tags)}{matched}"
    if i1 > 0:
        result = re.sub(rf'<(h1|h2|h3|h4|h5|h6|p|li|blockquote|a) number="{i1 - 1}"(.*?)>(.*?)</\1>', replace_callback, html, flags=re.DOTALL)
    else:
        result = re.sub(rf'<(h1|h2|h3|h4|h5|h6|p|li|blockquote|a) number="{i1}"(.*?)>(.*?)</\1>', replace_callback, html, flags=re.DOTALL)
    return result

with open(docx_current_version, "rb") as f:
    try:
        docx_current_version_html = mammoth.convert_to_html(f).value

    except Exception as e:
        print(f"Error converting .docx to HTML: {e}")
        sys.exit(1)

with open(commit_to_diff, "r", encoding="utf-8", newline="\n") as f:
    commit_html = f.read()

stripped_tags_commit = strip_tags(str(BeautifulSoup(commit_html, "html.parser")))

strip_tags_docx_current_version = strip_tags(str(BeautifulSoup(docx_current_version_html, "html.parser")))

p_in_commit = html_el_to_list(stripped_tags_commit)

p_in_docx_current_version = html_el_to_list(strip_tags_docx_current_version)

diff = difflib.SequenceMatcher(None, p_in_commit, p_in_docx_current_version)

diff_opcodes = diff.get_opcodes()

redline = stripped_tags_commit

for opcode in diff_opcodes:
    tag, i1, i2, j1, j2 = opcode
    substring_old = p_in_commit[i1:i2]
    substring_new = p_in_docx_current_version[j1:j2]

    if tag == "replace":
        redline = replace_tag(redline, substring_old, substring_new, i1)

    if tag == "delete":
        redline = delete_tag(redline, substring_old)

    if tag == "insert":
        redline = insert_tag(redline, substring_new, i1, strip_tags_docx_current_version)

with open("redline_diff.html", "w", encoding="utf-8") as f:
    f.write(redline)
