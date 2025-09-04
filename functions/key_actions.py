# functions/keyactions.py

def duplicate_line(TextArea):
    # Current line number from cursor
    line_num = int(TextArea.index("insert").split(".")[0])

    # Define the start and end of the current line
    line_start = f"{line_num}.0"
    line_end = f"{line_num}.0 lineend"

    # Always grab the full line text
    line_text = TextArea.get(line_start, line_end)

    # Ensure there’s room if it’s the last line
    if line_num == int(TextArea.index("end-1c").split(".")[0]):
        TextArea.insert("end", "\n")

    # Insert the duplicated line on the next line
    next_line_start = f"{line_num + 1}.0"
    TextArea.insert(next_line_start, line_text + "\n")

    # Place cursor at start of duplicated line
    TextArea.mark_set("insert", next_line_start)
    TextArea.see("insert")

# -------------------- File Operation Keybinds --------------------
def bind_file_shortcuts(root, TextArea, update_line_numbers_func, update_statusbar_func, app,
                        newFile, openFile, saveFile, saveasFile):

    def _new_file(event=None):
        newFile(root, TextArea, update_line_numbers_func, update_statusbar_func, app)
        return "break"

    def _open_file(event=None):
        openFile(root, TextArea, update_line_numbers_func, update_statusbar_func, app)
        return "break"

    def _save_file(event=None):
        saveFile(root, TextArea, app)
        return "break"

    def _saveas_file(event=None):
        saveasFile(root, TextArea, app)
        return "break"

    def _undo(event=None):
        try:
            TextArea.edit_undo()
        except Exception:
            pass
        return "break"

    def _redo(event=None):
        try:
            TextArea.edit_redo()
        except Exception:
            pass
        return "break"

    # File key bindings
    root.bind("<Control-n>", _new_file)
    root.bind("<Control-o>", _open_file)
    root.bind("<Control-s>", _save_file)
    root.bind("<Control-Shift-S>", _saveas_file)  # Ctrl+Shift+S

    # Undo/Redo bindings
    root.bind("<Control-z>", _undo)
    root.bind("<Control-Shift-Z>", _redo) # Ctrl+Shift+Z

    return {
        "new": _new_file,
        "open": _open_file,
        "save": _save_file,
        "saveas": _saveas_file,
        "undo": _undo,
        "redo": _redo,
    }

def track_text_modifications(TextArea, app):
    def on_modified(event):
        app.text_modified = True
        # Reset Tkinter's internal modified flag
        TextArea.edit_modified(False)
    TextArea.bind("<<Modified>>", on_modified)