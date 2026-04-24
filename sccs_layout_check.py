import os
from pathlib import Path
import sys
from default_css_styles import styles

directory_path = os.getcwd()

path = os.path.join(directory_path, f"{os.path.basename(directory_path)}.docx")

sccs_dir = os.path.join(directory_path, ".sccs")

def check_sccs():

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

    if not Path(os.path.join(sccs_dir, "data-commits")).is_dir():
        print("Commits data directory not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
        sys.exit(1)

    if not Path(os.path.join(sccs_dir, "data-commits", "txt-commits")).is_dir():
        print("Text commits directory not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
        sys.exit(1)

    if not Path(os.path.join(sccs_dir, "data-commits", "docx-commits")).is_dir():
        print("Docx commits directory not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
        sys.exit(1)

    if not Path(os.path.join(sccs_dir, "data-commits", "html-commits")).is_dir():
        print("HTML commits directory not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
        sys.exit(1)

    if not Path(os.path.join(sccs_dir, "view-commits")).is_dir():
        print("View commits directory not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
        sys.exit(1)

    if not Path(os.path.join(sccs_dir, "view-commits", "html-commits")).is_dir():
        print("View HTML commits directory not found. Please run 'sccs init <file_path>' to initialize SCCS for this file.")
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

    if not Path(path).is_file():
        print("Docx file not found. Re-initialize SCCS for this file with 'sccs init <file_path>'")
        sys.exit(1)

def wrap_html(html):
    return f"<!DOCTYPE html><html><head><meta charset='UTF-8'>{styles}</head><body><div class='center'><div id='target'>{html}</div></div></body></html>"