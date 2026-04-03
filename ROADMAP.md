# 📖 Roadmap

## 🚧 List of Commands to make

* sccs init
* sccs commit
* sccs revert

## 💡 Commands in detail:

### SCCS init

From a .docx, parse the file with docx2txt, a create a duplicated version in a folder named .sccs and store it in the unzipped version of .docx. Inside .sccs, along with the .txt file, store a history.xml file with the history data of the .docx. 

### SCCS commit

From an already initialized .docx, parse the file with docx2txt, create a duplicated version in the .sccs folder, and update the history.xml file with the new changes, and order them chronologically.

### SCCS revert

From an already initialized .docx, revert the file to a previous version stored in the .sccs folder, and update the history.xml file to reflect the reverted changes.
