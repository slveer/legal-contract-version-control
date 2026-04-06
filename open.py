from docx import Document
import sys

# Get user inputted path argument
path = sys.argv[2] if len(sys.argv) > 2 else None

# Strip .docx extension from the file name to create a directory
if not path:
    print("No file path provided")
    sys.exit(1)

with open(path, 'r') as file:
    commit = file.read()
document = Document()
document.add_paragraph(commit)
document.save('wip.docx')


