import os
import json
from tkinter import filedialog, messagebox, font as tkFont

CONFIG_FILE = "themes.json"

# ---------------- Theme Management ----------------
def apply_theme(theme_file, app):
    try:
        with open(theme_file, "r", encoding="utf-8") as f:
            theme = json.load(f)
    except Exception as e:
        messagebox.showerror("Theme Error", f"Could not load theme:\n{e}")
        return

    # Apply to editor (keep user's font, only change colors)
    app.TextArea.config(
        bg=theme.get("editor_bg", "#1e1e1e"),
        fg=theme.get("editor_fg", "#d4d4d4"),
        insertbackground=theme.get("cursor_color", "white")
    )

    # Line numbers (if present)
    if hasattr(app, "LineNumbers"):
        app.LineNumbers.config(
            bg=theme.get("line_numbers_bg", "#252526"),
            fg=theme.get("line_numbers_fg", "#858585")
        )

    # Status bar (if present)
    if hasattr(app, "StatusBar"):
        app.StatusBar.config(
            bg=theme.get("statusbar_bg", "#2d2d30"),
            fg=theme.get("statusbar_fg", "#d4d4d4")
        )

    # Save current theme path
    save_selected_theme(theme_file)
    print(f"[DEBUG] Applied theme: {theme.get('name', os.path.basename(theme_file))}")

def load_theme(app):
    filepath = filedialog.askopenfilename(
        defaultextension=".json",
        filetypes=[("Theme Files", "*.json")]
    )
    if filepath:
        apply_theme(filepath, app)


def save_selected_theme(path):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({"last_theme": path}, f)
    except Exception as e:
        print("Error saving theme:", e)


def load_saved_theme(app):
    if os.path.exists(CONFIG_FILE) and os.path.getsize(CONFIG_FILE) > 0:
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if "last_theme" in data and os.path.exists(data["last_theme"]):
                apply_theme(data["last_theme"], app)
        except Exception as e:
            print("Error loading saved theme:", e)


def unload_theme(app):
    # Reset to default theme
    app.TextArea.config(
        bg="#1e1e1e", fg="#d4d4d4",
        font=("Arial", 13), insertbackground="white"
    )
    app.current_font = ("Arial", 13)
    print("[DEBUG] Reverted to default theme")

    # Clear saved theme
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)
