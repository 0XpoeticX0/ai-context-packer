#!/usr/bin/env python3
"""
AI Context Packer
A lightweight developer tool that packages multi-directory project codebases 
into a clean, LLM-ready context document with security safeguards, directory tree maps,
and token telemetry.
"""

import os
import sys
import argparse
import fnmatch

# Force standard output to UTF-8 on Windows terminals
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

IGNORE_DIRS = {
    '.git', 'node_modules', '__pycache__', 'venv', 'env', '.env',
    '.idea', '.vscode', 'build', 'dist', '.dart_tool', '.next', '.cache',
    'coverage', '.pytest_cache', '.turbo', '.gradle'
}

IGNORE_EXTS = {
    '.jpg', '.jpeg', '.png', '.gif', '.ico', '.pdf', '.zip', '.tar', 
    '.gz', '.exe', '.dll', '.so', '.pyc', '.class', '.mp4', '.mp3', 
    '.wav', '.woff', '.woff2', '.ttf', '.eot', '.lock', '.svg', '.bin'
}

SENSITIVE_PATTERNS = {
    '.env*', '*.pem', '*.key', '*id_rsa*', 'credentials.json', 
    'service-account*.json', '*.secret', 'id_ed25519*'
}

OUTPUT_PATTERNS = {
    '*_context.txt', '*_context.md', 'ai_context.txt', 'ai_context.md'
}

# Mapping common file extensions to markdown syntax highlighting identifiers
LANG_MAP = {
    '.py': 'python',
    '.dart': 'dart',
    '.js': 'javascript',
    '.jsx': 'jsx',
    '.ts': 'typescript',
    '.tsx': 'tsx',
    '.java': 'java',
    '.c': 'c',
    '.cpp': 'cpp',
    '.h': 'c',
    '.hpp': 'cpp',
    '.cs': 'csharp',
    '.go': 'go',
    '.rs': 'rust',
    '.rb': 'ruby',
    '.php': 'php',
    '.swift': 'swift',
    '.kt': 'kotlin',
    '.html': 'html',
    '.css': 'css',
    '.scss': 'scss',
    '.json': 'json',
    '.yaml': 'yaml',
    '.yml': 'yaml',
    '.md': 'markdown',
    '.sql': 'sql',
    '.sh': 'bash',
    '.bash': 'bash',
    '.ps1': 'powershell'
}

def is_sensitive(filename):
    """Check if file matches sensitive credential or secret patterns."""
    return any(fnmatch.fnmatch(filename.lower(), p) for p in SENSITIVE_PATTERNS)

def is_packer_output(filename):
    """Check if file matches previously generated packer outputs."""
    return any(fnmatch.fnmatch(filename.lower(), p) for p in OUTPUT_PATTERNS)

def generate_directory_tree(start_path, max_depth=3):
    """Generates an ASCII visual representation of the project hierarchy."""
    tree_lines = [f"{os.path.basename(os.path.abspath(start_path))}/"]
    
    def walk(directory, prefix="", current_depth=1):
        if current_depth > max_depth:
            return
        try:
            entries = sorted(os.listdir(directory))
        except PermissionError:
            return
            
        filtered = [e for e in entries if e not in IGNORE_DIRS and not is_sensitive(e)]
        for i, entry in enumerate(filtered):
            is_last = (i == len(filtered) - 1)
            connector = "└── " if is_last else "├── "
            path = os.path.join(directory, entry)
            tree_lines.append(f"{prefix}{connector}{entry}{'/' if os.path.isdir(path) else ''}")
            if os.path.isdir(path):
                extension = "    " if is_last else "│   "
                walk(path, prefix + extension, current_depth + 1)

    walk(start_path)
    return "\n".join(tree_lines)

def pack_codebase(target_dir, output_path=None, as_markdown=True):
    """
    Scans project directory, ignores binaries and secrets, and writes
    a unified context file formatted for LLMs.
    """
    target_dir = os.path.abspath(target_dir)
    if not os.path.exists(target_dir):
        print(f"[ERROR] Target path does not exist: {target_dir}")
        return

    ext = ".md" if as_markdown else ".txt"
    if not output_path:
        project_name = os.path.basename(target_dir) or "project"
        output_path = os.path.join(os.getcwd(), f"{project_name}_context{ext}")

    print(f"\n==================================================")
    print(f" AI Context Packer")
    print(f"==================================================")
    print(f"Scanning target:  {target_dir}")
    print(f"Output document:  {output_path}\n")

    total_chars = 0
    file_count = 0
    skipped_sensitive = 0

    try:
        with open(output_path, 'w', encoding='utf-8') as out:
            # Header metadata
            project_title = os.path.basename(target_dir) or "Project"
            out.write(f"# Codebase Context: {project_title}\n\n")
            out.write("## Project Directory Tree\n```text\n")
            out.write(generate_directory_tree(target_dir))
            out.write("\n```\n\n---\n\n## Source Code Files\n\n")

            for root_dir, dirs, files in os.walk(target_dir):
                dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
                
                for file in files:
                    if is_sensitive(file):
                        skipped_sensitive += 1
                        print(f"  [GUARD] Skipped sensitive file: {file}")
                        continue

                    if is_packer_output(file):
                        continue

                    _, file_ext = os.path.splitext(file)
                    if file_ext.lower() in IGNORE_EXTS:
                        continue

                    full_path = os.path.join(root_dir, file)
                    if os.path.abspath(full_path) == os.path.abspath(output_path):
                        continue

                    rel_path = os.path.relpath(full_path, target_dir)

                    try:
                        with open(full_path, 'r', encoding='utf-8') as src:
                            content = src.read()

                        if as_markdown:
                            lang = LANG_MAP.get(file_ext.lower(), file_ext.lstrip('.').lower() or 'text')
                            out.write(f"### File: `{rel_path}`\n```{lang}\n{content}\n```\n\n")
                        else:
                            out.write(f"{'=' * 60}\nFILE PATH: {rel_path}\n{'=' * 60}\n{content}\n\n")

                        file_count += 1
                        total_chars += len(content)
                        print(f"  + Added: {rel_path}")

                    except UnicodeDecodeError:
                        continue  # Skip binary file
                    except Exception as err:
                        print(f"  ! Skipped ({err}): {rel_path}")

        est_tokens = total_chars // 4
        print(f"\n--------------------------------------------------")
        print(f"[SUCCESS] Packed {file_count} files into '{os.path.basename(output_path)}'.")
        if skipped_sensitive > 0:
            print(f"[SECURITY] {skipped_sensitive} sensitive credential files protected.")
        print(f"[TELEMETRY] ~{total_chars:,} characters | ~{est_tokens:,} estimated tokens.")
        print(f"[PATH] Full output saved to: {output_path}")
        print(f"--------------------------------------------------\n")

    except Exception as e:
        print(f"[ERROR] Failed to generate context file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Pack a codebase into a single AI-ready context document.")
    parser.add_argument("path", nargs="?", default=None, help="Path to project directory (optional, opens GUI if omitted)")
    parser.add_argument("-o", "--output", help="Custom output file path")
    parser.add_argument("--txt", action="store_true", help="Output as plain text instead of Markdown")
    args = parser.parse_args()

    target_path = args.path

    if not target_path:
        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            print("Opening folder selection dialog...")
            target_path = filedialog.askdirectory(title="Select Project Directory to Pack for AI")
            if not target_path:
                print("[INFO] No folder selected. Exiting.")
                return
        except Exception:
            print("[INFO] No GUI available. Pass the path as an argument: python ai_context_packer.py <path>")
            return

    if target_path:
        pack_codebase(target_path, output_path=args.output, as_markdown=not args.txt)

if __name__ == "__main__":
    main()
