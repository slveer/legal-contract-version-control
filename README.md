# 🎯 Simple Contracts Communication System, or SCCS

A lightweight distributed version control system designed to help legal professionals easily view and understand different versions of .docx and .pdf files.

## ⚠️ Please Read
- Build Status: Pre-Alpha
- License: GPLv3


---

## 📁 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Installation](#-installation)
- [Contributing](#-contributing)
- [Roadmap](#%EF%B8%8F-roadmap)
- [License](#-license)
- [Contact](mailto:danielaphillion@gmail.com)

## 🧠 About

- While there are many different version control systems, many struggle to track diff of .docx and .pdf files, because they are binary files. SCCS solves this by converting .pdf and .docx to .txt files, a keeping a .txt after each commit.
  
- SCCS is for legal professionals searching for a better way to track and view file changes of contracts.
  
- Currently, most version control for contracts is just multiple versions of mostly identical files, emailed back and forth between people. Storing .txt files and keeping less XML metadata as files can share it. It also cleanly shows diff between version of a file, instead of between different files

## ✨ Features

- Command line tools to initialize, commit, and revert (currently in progress)

## 🚧 Features to Make 

- **See Roadmap for more details**

- Host repository online like Git

- Different Branches

- Graphic diff viewer between .txt files

## 📦 Installation

```bash
# Clone the Git Repository
git clone https://github.com/slveer/legal-contract-version-control.git

# Install all required dependencies
pip install -r requirements.txt
```


- No features are fully functional at this time, will update installation guide ASAP

## 🤝 Contributing
Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) for info on how to get started contributing! It is greatly appreciated 😁 !

## 🗺️ Roadmap
The full roadmap is avaliable in [ROADMAP.md](ROADMAP.md)

## 📃 License
SCCS uses the GPLv3, which you can find in [LICENSE](LICENSE)
