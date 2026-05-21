MESSAGES_TO_PRINT = [
    "SCCS Help", "Available commands:",
    "  init    - Initialize a new SCCS repository",
    "  commit  - Commit changes to a repository",
    "  open    - Restore a previous commit and overwrite the current changes",
    "  log     - Show commit history",
    "  diff    - Compare the current .docx converted to HTML with a specified commit .html file",
    "  status  - Show the status of a repository",
    "  help    - Show this help message"
]

def print_items():
    for item in MESSAGES_TO_PRINT:
        print(item)

print_items()





