import os
from pathlib import Path
import sys
from bs4 import BeautifulSoup
import mammoth
import difflib
from sccs_layout_check import check_sccs
from default_css_styles import styles



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

check_sccs()

try:
    with open(docx_current_version, "rb") as f:
        docx_current_version_html = mammoth.convert_to_html(f).value

except Exception as e:
    print(f"Error converting .docx to HTML: {e}")
    sys.exit(1)


try:
    with open(commit_to_diff, "r", encoding="utf-8", newline="\n") as f:
        commit_html = f.read()
except Exception as e:
    print(f"Error reading commit file: {e}")
    sys.exit(1)

def remove_inline_semantics(html):
    soup = html
    for tag in soup.find_all():
        if tag.name in ["b", "i", "u", "strong", "em"]:
            tag.unwrap()
        
        if tag.name == "style":
            tag.decompose()
            continue
    return soup

def number_tags(html):
    soup = html
    for i, tag in enumerate(soup.find_all()):
        if tag.name == "style":
            continue
        tag['data-number'] = str(i)
    return soup

def tags_to_list(html):
    soup = html
    return [str(tag) for tag in soup.find_all()]

def get_data_number(tag_list):
    data_number = set()
    for tag in tag_list:
        parsed_tag = tag if hasattr(tag, 'attrs') else BeautifulSoup(tag, "html.parser").find()
        if parsed_tag is not None:
            if parsed_tag.get('data-number') is not None:
                data_number.add(parsed_tag.get('data-number'))
    return data_number

docx_current_version_list = tags_to_list(number_tags(remove_inline_semantics(docx_current_version_html)))

commit_list = tags_to_list(number_tags(remove_inline_semantics(commit_html)))

opcodes = difflib.SequenceMatcher(None, tags_to_list(remove_inline_semantics(commit_html)), tags_to_list(remove_inline_semantics(docx_current_version_html))).get_opcodes()

redline = BeautifulSoup(number_tags(remove_inline_semantics(commit_html)), "html.parser")

def delete_tag(html, old_changed_strings):
    old_data_numbers = get_data_number(old_changed_strings)
    soup = html
    for tag in soup.find_all():
        if tag.name == 'style':
            tag.decompose()
            continue

        if tag.get('data-number') in old_data_numbers:
            if 'class' in tag.attrs:
                tag['class'].append('deleted')
            else:
                tag['class'] = ['deleted']
    return soup

def replace_tag(html, old_changed_strings, new_changed_strings):
    old_data_numbers = get_data_number(old_changed_strings)
    frag = BeautifulSoup("".join(new_changed_strings), "html.parser")
    soup = html
    match = []
    for tag in soup.find_all():
        
        if tag.name == 'style':
            tag.decompose()
            continue
        if tag.get('data-number') in old_data_numbers:
            match.append(tag)

    for i in frag.find_all():
        if i.name:
            if 'class' in i.attrs:
                i['class'].append('inserted')
            else:
                i['class'] = ['inserted']
    
    if match:
        match[-1].insert_after(frag)
        for tag in match:
            if 'class' in tag.attrs:
                tag['class'].append('deleted')
            else:
                tag['class'] = ['deleted']
    return soup

def insert_tag(html, new_changed_strings, i1):
    soup = html
    for tag in soup.find_all():
        if tag.name == 'style':
            tag.decompose()
            continue
    tags = soup.find_all()
    frag = BeautifulSoup("".join(new_changed_strings), "html.parser")
    for i in frag.find_all():
        if i.name:
            if 'class' in i.attrs:
                i['class'].append('inserted')
            else:
                i['class'] = ['inserted']
    if i1 < len(tags):
        tags[i1].insert_before(frag)
    else:
        soup.append(frag)    
    
    return soup

for opcode in reversed(opcodes):
    tag, i1, i2, j1, j2 = opcode
    
    old_changed_strings = commit_list[i1:i2]
    new_changed_strings = docx_current_version_list[j1:j2]
    if tag == "replace":
        redline = replace_tag(redline, old_changed_strings, new_changed_strings)
    if tag =="insert":
        redline = insert_tag(redline, new_changed_strings, i1)
    if tag =="delete":
        redline = delete_tag(redline, old_changed_strings)
with open("redline.html", "w", encoding="utf-8", newline="\n") as f:
    f.write(f"{styles}\n{str(redline)}")