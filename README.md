# 🎯 Simple Contracts Communication System, or SCCS

A lightweight distributed version control system designed to help legal professionals easily view and understand different versions of .docx files currently. ( .pdf files planned)

## ⚠️ Please Read
- Build Status: Pre-Alpha
- License: GPLv3


---

## 📁 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Installation](#-installation)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](mailto:danielaphillion@gmail.com)

## 🧠 About

- While there are many different version control systems, many struggle to track diffs in .docx and .pdf files because they are binary. SCCS solves this by converting .pdf and .docx files to .txt and keeping a .txt version after each commit.
  
- SCCS is for legal professionals searching for a better way to track and view file changes of contracts.
  
- Currently, most version control for contracts is just multiple versions of mostly identical files, emailed back and forth between people. Storing .txt files and keeping less XML metadata as files can share it. It also cleanly shows diff between version of a file, instead of between different files

## ✨ Features

CLI interface to:

- Initalize new docx

- Commit changes to an existing docx

- Compare the current version of the docx to an earlier commit in HTML

- Open previous commits

- View a history log of all commits

- Check the status (i.e. have there been changes)

- Get help/tips (i.e. lists all commands and their function)


## 🚧 Features Coming Soon (WIP)

- Host repository online like Git

- Different Branches

## 📦 Installation

```bash
# Clone the Git Repository
git clone https://github.com/slveer/legal-contract-version-control.git

# Install all required dependencies
pip install -r requirements.txt
```

## 🤝 Contributing
Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) for info on how to get started contributing! It is greatly appreciated 😁 !

## 📃 License
SCCS uses the GPLv3, which you can find in [LICENSE](LICENSE)
