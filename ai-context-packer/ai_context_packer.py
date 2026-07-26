import os
import sys
import tkinter as tk
from tkinter import filedialog

# ---------------------------------------------------------
# NUCLEAR OPTION FOR WINDOWS TERMINALS:
# Force standard output to UTF-8 to prevent charmap crashes
# ---------------------------------------------------------
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

def get_script_directory():
    """Returns the directory where this Python script is located."""
    return os.path.dirname(os.path.abspath(__file__))

def consolidate_files_for_ai():
    """
    Opens a UI to select a directory, reads all text files inside, 
    and writes them to a single formatted text file next to this script.
    """
    root = tk.Tk()
    root.withdraw() 
    
    print("Opening folder selection dialog...")
    target_directory = filedialog.askdirectory(title="Select Folder to Pack for AI")
    
    if not target_directory:
        print("[INFO] No folder selected. Exiting.")
        return

    output_filename = os.path.join(get_script_directory(), "ai_context.txt")
    
    ignore_exts = {
        '.jpg', '.jpeg', '.png', '.gif', '.ico', '.pdf', '.zip', '.tar', 
        '.gz', '.exe', '.dll', '.so', '.pyc', '.class', '.mp4', '.mp3', 
        '.wav', '.woff', '.woff2', '.ttf', '.eot'
    }
    
    ignore_dirs = {
        '.git', 'node_modules', '__pycache__', 'venv', 'env', 
        '.idea', '.vscode', 'build', 'dist', '.dart_tool'
    }

    print(f"\nScanning directory: {os.path.abspath(target_directory)}")
    print(f"Output will be saved to: {output_filename}\n")
    
    try:
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            outfile.write(f"# Codebase Context Consolidation\n")
            outfile.write(f"# Source Directory: {os.path.abspath(target_directory)}\n\n")
            
            file_count = 0
            
            for root_dir, dirs, files in os.walk(target_directory):
                dirs[:] = [d for d in dirs if d not in ignore_dirs]
                
                for file in files:
                    _, ext = os.path.splitext(file)
                    
                    if ext.lower() in ignore_exts:
                        continue
                        
                    file_path = os.path.join(root_dir, file)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            content = infile.read()
                        
                        outfile.write(f"{'=' * 60}\n")
                        outfile.write(f"FILE PATH: {file_path}\n")
                        outfile.write(f"{'=' * 60}\n\n")
                        outfile.write(f"{content}\n\n")
                        
                        file_count += 1
                        print(f"Added: {file_path}")
                        
                    except UnicodeDecodeError:
                        print(f"Skipped (Binary/Encoding issue): {file_path}")
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")

        print(f"\n[SUCCESS] {file_count} files consolidated.")
        print(f"[FILE SAVED] {output_filename}")
        
    except Exception as e:
        print(f"[ERROR] Error creating output file: {e}")

if __name__ == "__main__":
    consolidate_files_for_ai()