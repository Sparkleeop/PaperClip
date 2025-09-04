from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import END, messagebox
import os
import json

file = None

# ---------------- Project-local Paths ----------------
APP_DATA_DIR = os.path.join(os.path.dirname(__file__), "..")  # project root
LAST_FILE = os.path.join(APP_DATA_DIR, "last_file.json")
RECENT_FILES = os.path.join(APP_DATA_DIR, "recent_files.json")
MAX_RECENT_FILES = 10

# ---------------- File Operations ----------------
def newFile(root, TextArea, update_line_numbers, update_statusbar, app=None):
    global file
    if app and getattr(app, "text_modified", False):
        if not _prompt_save(root, TextArea, app):
            return
    root.title("Untitled - PaperClip by Sparklee")
    file = None
    TextArea.delete(1.0, END)
    update_line_numbers()
    update_statusbar()
    if app:
        app.text_modified = False
        TextArea.config(font=app.current_font)

def openFile(root, TextArea, update_line_numbers, update_statusbar, app=None, path=None):
    global file
    if app and getattr(app, "text_modified", False):
        if not _prompt_save(root, TextArea, app):
            return

    if path:
        file = path
    else:
        file = askopenfilename(defaultextension=".txt",
                               filetypes=[("All files", "*.*"), ("Text Documents", "*.txt")])
        if not file:
            file = None
            return

    # Update window title
    root.title(os.path.basename(file) + " - PaperClip by Sparklee")
    TextArea.delete(1.0, END)
    with open(file, "r", encoding="utf-8", errors="replace") as f:
        TextArea.insert(1.0, f.read())

    update_line_numbers()
    update_statusbar()
    if app:
        app.text_modified = False
        TextArea.config(font=app.current_font)
        app.file = file  # Update app context

    # Track as recent + last opened
    save_last_file(file)
    add_recent_file(file)

def saveFile(root, TextArea, app=None):
    global file
    if file is None:
        return saveasFile(root, TextArea, app)

    with open(file, "w", encoding="utf-8") as f:
        f.write(TextArea.get(1.0, END))
    root.title(os.path.basename(file) + " - PaperClip by Sparklee")
    save_last_file(file)
    add_recent_file(file)
    if app:
        app.text_modified = False

def saveasFile(root, TextArea, app=None):
    global file
    file = asksaveasfilename(initialfile="Untitled.txt", defaultextension=".txt",
                             filetypes=[("All files", "*.*"), ("Text Documents", "*.txt")])
    if not file:
        return
    with open(file, "w", encoding="utf-8") as f:
        f.write(TextArea.get("1.0", "end-1c"))
    root.title(f"{file} - PaperClip by Sparklee")
    save_last_file(file)
    add_recent_file(file)
    if app:
        app.text_modified = False

def quitApp(root, TextArea=None, app=None):
    if app and getattr(app, "text_modified", False):
        if not _prompt_save(root, TextArea, app):
            return
    root.destroy()

# ---------------- Internal Helpers ----------------
def _prompt_save(root, TextArea, app):
    response = messagebox.askyesnocancel(
        "Unsaved Changes",
        "You have unsaved changes. Do you want to save before continuing?"
    )
    if response is None:  # Cancel
        return False
    elif response:  # Yes
        saveFile(root, TextArea, app)
    return True

def save_last_file(path):
    try:
        with open(LAST_FILE, "w", encoding="utf-8") as f:
            json.dump({"last_file": path}, f)
        print(f"[DEBUG] Saved last_file.json: {path}")
    except Exception as e:
        print(f"Error saving last file: {e}")

def load_last_file():
    try:
        if os.path.exists(LAST_FILE):
            with open(LAST_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data.get("last_file")
                else:
                    # wrong type -> reset
                    return None
    except Exception as e:
        print(f"Error loading last file: {e}")
    return None

# ---------------- Recent Files ----------------
def load_recent_files():
    if os.path.exists(RECENT_FILES):
        try:
            with open(RECENT_FILES, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_recent_files(files):
    try:
        with open(RECENT_FILES, "w", encoding="utf-8") as f:
            json.dump(files, f)
        print(f"[DEBUG] Updated recent_files.json: {files}")
    except Exception as e:
        print(f"Error saving recent files: {e}")

def add_recent_file(path):
    recent = load_recent_files()
    if path in recent:
        recent.remove(path)
    recent.insert(0, path)
    recent = recent[:MAX_RECENT_FILES]
    save_recent_files(recent)
