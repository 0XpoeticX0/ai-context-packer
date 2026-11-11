# AI Context Packer 📦

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Clean](https://img.shields.io/badge/Code%20Style-Black-000000.svg)](https://github.com/psf/black)

A lightweight developer productivity utility that recursively traverses multi-directory project codebases and packs them into a single structured, LLM-ready context document.

Built for seamless ingestion into **ChatGPT, Claude 3.5 Sonnet, Gemini 1.5/2.0, Cursor, Copilot, and Local LLMs (Ollama / vLLM)**.

---

## ⚡ Why Use AI Context Packer?

When asking LLMs to debug, refactor, or architect features across a project, manually copy-pasting individual files breaks context and wastes time. 

**AI Context Packer** solves this with one command or click:
1. **Generates an ASCII Project Tree** at the top of the context file so the model understands your architecture immediately.
2. **Normalizes Relative Paths** (`lib/screens/home.dart` instead of local `C:\Users\...` paths), protecting privacy and saving context tokens.
3. **Sensitive File Guard** automatically skips `.env*`, `.pem`, `.key`, and credential files to prevent accidental API key leaks.
4. **Markdown Syntax Highlighting** wraps code in language-specific code blocks (`python`, `dart`, `typescript`, etc.) for optimal model tokenization.
5. **Real-time Telemetry** calculates character counts and estimated tokens so you know whether your codebase fits within your model's context window.

---

## 🚀 Key Features

* 🛡️ **Sensitive File Guard:** Automatically detects and skips `.env`, `.pem`, `.key`, `id_rsa`, `credentials.json`, and secrets.
* 🌳 **ASCII Directory Tree:** Injects a clean visual map of your project structure before source files.
* 🖥️ **Dual Interface (CLI + GUI):** Pass arguments via terminal or leave them blank to open an interactive folder picker.
* 📝 **Markdown or Plain Text:** Outputs clean Markdown with language-specific syntax fences by default (or `--txt` for plain text).
* 📊 **Token Telemetry:** Reports estimated token counts upon completion.
* ⚡ **Zero Third-Party Dependencies:** Uses pure Python standard library (`argparse`, `os`, `fnmatch`, `tkinter`).

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/0XpoeticX0/ai-context-packer.git
cd ai-context-packer
```

*(No `pip install` required — runs immediately with standard Python 3.8+)*

---

## 💻 Usage

### 1. Command Line Interface (CLI)

Pack any directory by passing its path:

```bash
# Pack the current directory into Markdown
python ai_context_packer.py .

# Pack a specific project folder
python ai_context_packer.py /path/to/my-project

# Specify custom output file
python ai_context_packer.py /path/to/my-project -o my_context.md

# Output as plain text instead of Markdown
python ai_context_packer.py /path/to/my-project --txt
```

### 2. Graphical Interface (GUI)

Run without arguments to launch the native folder picker:

```bash
python ai_context_packer.py
```

---

## 📄 Example Output

````markdown
# Codebase Context: FlutterApp

## Project Directory Tree
```text
FlutterApp/
├── lib/
│   ├── main.dart
│   └── screens/
│       └── home.dart
└── pubspec.yaml
```

---

## Source Code Files

### File: `lib/main.dart`
```dart
import 'package:flutter/material.dart';

void main() => runApp(const MyApp());
...
```
````

---

## 🚫 Automatically Ignored Files & Directories

* **Build & Cache:** `.git`, `node_modules`, `__pycache__`, `venv`, `.dart_tool`, `build`, `dist`, `.next`, `.gradle`, `.turbo`
* **Binaries & Media:** `.jpg`, `.png`, `.pdf`, `.zip`, `.exe`, `.dll`, `.so`, `.mp4`, `.mp3`, `.woff`, `.ttf`
* **Secrets & Keys:** `.env*`, `*.pem`, `*.key`, `*id_rsa*`, `credentials.json`, `service-account*.json`

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/0XpoeticX0/ai-context-packer/issues).

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
