import os
import sys
from tkinter import *
from tkinter.messagebox import askyesno, showinfo

# ----------------- DPI / Scaling Fix -----------------
if sys.platform == "win32":
    try:
        import ctypes
        # Enable DPI awareness before Tk initializes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # SYSTEM_DPI_AWARE
    except Exception:
        pass

# -------------------- Initialize Tkinter --------------------
root = Tk()
root.title("Untitled - PaperClip by Sparklee")
root.iconbitmap("C:/Users/User 1/OneDrive - Sellability PS/Documents/Sparsh/NotePAD/assets/icon.ico")
root.geometry("1280x720")
root.minsize(600, 400)

version = "1.2.3-Alpha"

# Adjust scaling dynamically
try:
    scaling = root.winfo_fpixels('1i') / 72  # pixels per inch / 72 = scaling factor
    root.tk.call('tk', 'scaling', scaling)
except Exception:
    root.tk.call('tk', 'scaling', 1.0)  # fallback

try:
    scaling = root.tk.call('tk', 'scaling')
except Exception:
    scaling = 1.0

# -------------------- Imports for modular functions --------------------
from functions.file_ops import newFile, openFile, saveFile, saveasFile, quitApp, load_last_file, load_recent_files, save_recent_files
from functions.edit_ops import cut, copy, paste, delete_previous_word
from functions.view_ops import toggle_fullscreen, exit_fullscreen
from functions.statusbar import update_statusbar
from functions.line_numbers import update_line_numbers
from functions.plugins import load_plugins, unload_plugins, load_saved_plugins
from functions.styling_ops import set_font, toggle_bold, toggle_italic, toggle_underline, apply_heading, set_alignment, set_text_color, set_highlight_color, toggle_bullet , toggle_numbered_list , handle_auto_bullet , clear_formatting
from functions.key_actions import duplicate_line, bind_file_shortcuts

# -------------------- Editor Frame --------------------
editor_frame = Frame(root)
editor_frame.pack(expand=True, fill=BOTH)


# Line Numbers
line_numbers = Canvas(editor_frame, width=60, background="#252526", highlightthickness=0)
line_numbers.pack(side=LEFT, fill=Y)

# Main Text Area
default_font_size = 13 
TextArea = Text(
    editor_frame,
    font=("Arial", default_font_size),
    bg="#1e1e1e",
    fg="#d4d4d4",
    insertbackground="white",
    undo=True,            
    autoseparators=True,    
    maxundo=-1              
)
TextArea.pack(side=LEFT, expand=True, fill=BOTH)

TextArea.bind("<Control-BackSpace>", lambda e: delete_previous_word(TextArea))
TextArea.bind("<Return>", lambda e: handle_auto_bullet(e, TextArea))

# Scrollbar
scroll = Scrollbar(editor_frame, command=TextArea.yview)
scroll.pack(side=RIGHT, fill=Y)
TextArea.config(yscrollcommand=scroll.set)

# -------------------- Update Functions --------------------
lines_var = StringVar(value="Lines: 1")
words_var = StringVar(value="Words: 0")

def combined_update(event=None):
    update_line_numbers_func()
    update_statusbar_func()

def on_text_modified(event=None):
    app.text_modified = True
    combined_update(event)

# -------------------- Wrapper Functions --------------------
update_line_numbers_func = lambda e=None: update_line_numbers(TextArea, line_numbers, e)
update_statusbar_func = lambda e=None: update_statusbar(TextArea, lines_var, words_var, e)

# Bindings
TextArea.bind("<MouseWheel>", combined_update)
TextArea.bind("<Button-1>", combined_update)
TextArea.bind("<Configure>", combined_update)
TextArea.bind("<<Change>>", combined_update)
TextArea.bind("<Expose>", combined_update)

def track_text_modifications(TextArea, app):
    def on_modified(event):
        app.text_modified = True
        # Reset Tkinter's internal modified flag so <<Modified>> triggers again
        TextArea.edit_modified(False)
    TextArea.bind("<<Modified>>", on_modified)


# Styling keybindings
def toggle_bold_event(event):
    toggle_bold(TextArea, app)
    return "break"

def toggle_italic_event(event):
    toggle_italic(TextArea, app)
    return "break"

def toggle_underline_event(event):
    toggle_underline(TextArea, app)
    return "break"

def _dup_line_event(e):
    duplicate_line(TextArea)
    return "break"  # IMPORTANT: stop default behavior


TextArea.bind("<Control-d>", _dup_line_event)
TextArea.bind("<Control-b>", toggle_bold_event)
TextArea.bind("<Control-i>", toggle_italic_event)
TextArea.bind("<Control-u>", toggle_underline_event)

# Scroll wiring
def _on_scrollbar(*args):
    TextArea.yview(*args)
    update_line_numbers_func()

def _on_text_yscroll(first, last):
    scroll.set(first, last)
    root.after_idle(update_line_numbers_func)

def _on_mousewheel(event):
    TextArea.yview_scroll(int(-event.delta/120), "units")
    update_line_numbers_func()
    return "break"

scroll.config(command=_on_scrollbar)
TextArea.config(yscrollcommand=_on_text_yscroll)
TextArea.bind("<MouseWheel>", _on_mousewheel)

update_line_numbers_func()

# -------------------- App Context --------------------
class AppContext:
    def __init__(self, root, text_area, extensions_menu, file_menu):
        self.root = root
        self.TextArea = text_area
        self.ExtensionsMenu = extensions_menu
        self.FileMenu = file_menu
        self.text_modified = False
        self.current_font = ("Arial", default_font_size)

# -------------------- Menu Bar --------------------
MenuBar = Menu(root)
root.config(menu=MenuBar)

# File Menu (created after TextArea and update functions)
FileMenu = Menu(MenuBar, tearoff=0)
FileMenu.add_command(label="New", command=lambda: newFile(root, TextArea, update_line_numbers_func, update_statusbar_func, app))
FileMenu.add_command(label="Open", command=lambda: openFile(root, TextArea, update_line_numbers_func, update_statusbar_func, app))
FileMenu.add_command(label="Save", command=lambda: saveFile(root, TextArea, app))
FileMenu.add_command(label="Save As", command=lambda: saveasFile(root, TextArea, app))
FileMenu.add_separator()
FileMenu.add_command(label="Exit", command=lambda: quitApp(root, TextArea, app))
# Recent Files submenu
RecentMenu = Menu(FileMenu, tearoff=0)
FileMenu.add_cascade(label="Open Recent", menu=RecentMenu)
MenuBar.add_cascade(label="File", menu=FileMenu)

def update_recent_menu():
    RecentMenu.delete(0, END)
    recent = load_recent_files()
    if not recent:
        RecentMenu.add_command(label="(No recent files)", state=DISABLED)
    else:
        for path in recent:
            RecentMenu.add_command(
                label=path,
                command=lambda p=path: openFile(root, TextArea, update_line_numbers_func, update_statusbar_func, app, path=p)
            )
        RecentMenu.add_separator()
        RecentMenu.add_command(label="Clear Recent", command=clear_recent_files)

def clear_recent_files():
    save_recent_files([])
    update_recent_menu()

# Initialize menu
update_recent_menu()

def safe_redo(text_widget):
    try:
        text_widget.edit_redo()
    except Exception:
        pass

# Edit Menu
EditMenu = Menu(MenuBar, tearoff=0)

# Undo / Redo
EditMenu.add_command(
    label="Undo",
    command=lambda: (TextArea.edit_undo() if TextArea.edit_modified() else None),
    accelerator="Ctrl+Z"
)

EditMenu.add_command(label="Redo", command=lambda: safe_redo(TextArea), accelerator="Ctrl+Y")
EditMenu.add_separator()
EditMenu.add_command(label="Cut", command=lambda: cut(TextArea), accelerator="Ctrl+X")
EditMenu.add_command(label="Copy", command=lambda: copy(TextArea), accelerator="Ctrl+C")
EditMenu.add_command(label="Paste", command=lambda: paste(TextArea), accelerator="Ctrl+V")
MenuBar.add_cascade(label="Edit", menu=EditMenu)

# Format Menu
FormatMenu = Menu(MenuBar, tearoff=0)
FormatMenu.add_command(label="Font...", command=lambda: set_font(TextArea, app))
FormatMenu.add_command(label="Bold", command=lambda: toggle_bold(TextArea, app))
FormatMenu.add_command(label="Italic", command=lambda: toggle_italic(TextArea, app))
FormatMenu.add_command(label="Underline", command=lambda: toggle_underline(TextArea, app))
FormatMenu.add_separator()
FormatMenu.add_command(label="Bulleted List", command=lambda: toggle_bullet(TextArea))
FormatMenu.add_command(label="Numbered List", command=lambda: toggle_numbered_list(TextArea))
FormatMenu.add_separator()

# Headings submenu
HeadingMenu = Menu(FormatMenu, tearoff=0)
HeadingMenu.add_command(label="Heading 1", command=lambda: apply_heading(TextArea, 1, app))
HeadingMenu.add_command(label="Heading 2", command=lambda: apply_heading(TextArea, 2, app))
HeadingMenu.add_command(label="Heading 3", command=lambda: apply_heading(TextArea, 3, app))
FormatMenu.add_cascade(label="Headings", menu=HeadingMenu)

# Alignment submenu
AlignMenu = Menu(FormatMenu, tearoff=0)
AlignMenu.add_command(label="Left", command=lambda: set_alignment(TextArea, "left"))
AlignMenu.add_command(label="Center", command=lambda: set_alignment(TextArea, "center"))
AlignMenu.add_command(label="Right", command=lambda: set_alignment(TextArea, "right"))
AlignMenu.add_command(label="Justify", command=lambda: set_alignment(TextArea, "justify"))
FormatMenu.add_cascade(label="Alignment", menu=AlignMenu)

# Colors submenu
ColorMenu = Menu(FormatMenu, tearoff=0)
ColorMenu.add_command(label="Text Color", command=lambda: set_text_color(TextArea))
ColorMenu.add_command(label="Highlight Color", command=lambda: set_highlight_color(TextArea))
FormatMenu.add_cascade(label="Colors", menu=ColorMenu)

# Clear formatting option
FormatMenu.add_separator()
FormatMenu.add_command(label="Clear Formatting", command=lambda: clear_formatting(TextArea))

# Add back to menubar
MenuBar.add_cascade(label="Format", menu=FormatMenu)

# Extensions Menu
ExtensionsMenu = Menu(MenuBar, tearoff=0)
ExtensionsMenu.add_command(label="Load Extension...", command=lambda: load_plugins(app))
ExtensionsMenu.add_command(label="Unload All Extensions", command=lambda: unload_plugins(app, clear_saved=True))
MenuBar.add_cascade(label="Extensions", menu=ExtensionsMenu)

# Help Menu
HelpMenu = Menu(MenuBar, tearoff=0)
HelpMenu.add_command(label="About PaperClip", command=lambda: showinfo("About PaperClip", "PaperClip by Sparklee"))
HelpMenu.add_command(label="Version info", command=lambda: showinfo("Version", version))
MenuBar.add_cascade(label="Help", menu=HelpMenu)

# -------------------- App Instance --------------------
app = AppContext(root, TextArea, ExtensionsMenu, FileMenu)
track_text_modifications(TextArea, app)

bind_file_shortcuts(root, TextArea, update_line_numbers_func, update_statusbar_func,
                    app, newFile, openFile, saveFile, saveasFile)

if len(sys.argv) > 1:
    path = sys.argv[1]
    if os.path.exists(path):
        try:
            openFile(root, TextArea, update_line_numbers_func, update_statusbar_func, app, path=path)
        except Exception as e:
            print(f"Failed to open file from command line: {e}")
else:
    last_file = load_last_file()
    if last_file and os.path.exists(last_file):
        openFile(root, TextArea, update_line_numbers_func, update_statusbar_func, app, path=last_file)

# Load saved plugins
load_saved_plugins(app)


# -------------------- Status Bar --------------------
statusbar = Frame(root, bd=1, relief=SUNKEN, bg="#2d2d30")
statusbar.pack(side=BOTTOM, fill=X)

Label(statusbar, textvariable=words_var, bg="#2d2d30", fg="#d4d4d4").pack(side=LEFT, padx=10)
Label(statusbar, textvariable=lines_var, bg="#2d2d30", fg="#d4d4d4").pack(side=LEFT, padx=10)
Label(statusbar, text="UTF-8", bg="#2d2d30", fg="#d4d4d4").pack(side=LEFT, padx=10)
Label(statusbar, text="Windows(CRLF)", bg="#2d2d30", fg="#d4d4d4").pack(side=LEFT, padx=10)

update_statusbar_func()

# -------------------- Exit Confirmation --------------------
def on_close():
    if app.text_modified:
        if askyesno("Unsaved Changes", "You have unsaved changes. Do you want to exit?"):
            root.destroy()
    else:
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

# -------------------- Fullscreen Bindings --------------------
root.bind("<F11>", lambda e: toggle_fullscreen(root))
root.bind("<Escape>", lambda e: exit_fullscreen(root))

# -------------------- Start App --------------------
root.mainloop()