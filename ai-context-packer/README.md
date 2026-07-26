# AI Context Packer

A lightweight Python utility that packages an entire project into a single text file, making it easy to share your codebase with AI assistants such as ChatGPT, Claude, Gemini, Cursor, Copilot, or local LLMs.

Instead of manually selecting dozens of files, AI Context Packer recursively scans your project and combines all readable source files into a single `ai_context.txt` file.

---

## Features

- Recursive project scanning
- Simple folder selection using a GUI
- UTF-8 output
- Automatically ignores:
  - `.git`
  - `node_modules`
  - `venv`
  - `__pycache__`
  - `.dart_tool`
  - `build`
  - `dist`
  - `.idea`
  - `.vscode`
- Skips binary files automatically
- Preserves original file paths
- No third-party dependencies
- Works out of the box with Python

---

## Example Output

```text
============================================================
FILE PATH: lib/main.dart
============================================================

import 'package:flutter/material.dart';

...

============================================================
FILE PATH: lib/screens/home.dart
============================================================

...
```

---

## Installation

```bash
git clone https://github.com/<your-username>/ai-context-packer.git
cd ai-context-packer
```

---

## Usage

Run:

```bash
python ai_context_packer.py
```

A folder picker will open.

1. Select your project folder.
2. Wait for the scan to complete.
3. An `ai_context.txt` file will be generated beside the script.

---

## Ignored Files

Binary files such as images, videos, audio, fonts, executables, and archives are skipped automatically.

Common development folders are also ignored to keep the output clean.

---

## Why?

Large language models work best when they have access to your project's source code.

Instead of uploading dozens or hundreds of files individually, AI Context Packer generates one structured context file that can be pasted or uploaded directly into AI tools.

Useful for:

- Flutter
- Python
- React
- Node.js
- Java
- C/C++
- General software projects

---

## Requirements

- Python 3.8+
- tkinter (included with most Python installations)

---

## Repository Structure

```text
ai-context-packer/
│
├── ai_context_packer.py
├── README.md
├── LICENSE
├── .gitignore
└── screenshots/
```

---

## License

MIT License
