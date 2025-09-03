from tkinter import *
from tkinter.messagebox import askyesno, showinfo
import os

# Import modular functions
from functions.file_ops import newFile, openFile, saveFile, saveasFile, quitApp, load_last_file
from functions.edit_ops import cut, copy, paste, delete_previous_word
from functions.view_ops import toggle_fullscreen, exit_fullscreen
from functions.statusbar import update_statusbar
from functions.line_numbers import update_line_numbers
from functions.plugins import load_plugins, unload_plugins, load_saved_plugins

# -------------------- Initialize Tkinter --------------------
root = Tk()
root.title("Untitled - PaperClip by Sparklee")
root.iconbitmap("C:/Users/User 1/OneDrive - Sellability PS/Documents/Sparsh/NotePAD/assets/icon.ico")
root.geometry("854x480")
root.minsize(600, 400)

# -------------------- Editor Frame --------------------
editor_frame = Frame(root)
editor_frame.pack(expand=True, fill=BOTH)

# Line Numbers
line_numbers = Canvas(editor_frame, width=60, background="#252526", highlightthickness=0)
line_numbers.pack(side=LEFT, fill=Y)

# Main Text Area
TextArea = Text(editor_frame, font="lucida 13", bg="#1e1e1e", fg="#d4d4d4", insertbackground="white")
TextArea.pack(side=LEFT, expand=True, fill=BOTH)
TextArea.bind("<Control-BackSpace>", lambda e: delete_previous_word(TextArea))

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
TextArea.bind("<KeyRelease>", on_text_modified)
TextArea.bind("<MouseWheel>", combined_update)
TextArea.bind("<Button-1>", combined_update)
TextArea.bind("<Configure>", combined_update)
TextArea.bind("<<Change>>", combined_update)
TextArea.bind("<Expose>", combined_update)

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
FileMenu.add_separator()
MenuBar.add_cascade(label="File", menu=FileMenu)

# Edit Menu
EditMenu = Menu(MenuBar, tearoff=0)
EditMenu.add_command(label="Cut", command=lambda: cut(TextArea))
EditMenu.add_command(label="Copy", command=lambda: copy(TextArea))
EditMenu.add_command(label="Paste", command=lambda: paste(TextArea))
EditMenu.add_separator()
MenuBar.add_cascade(label="Edit", menu=EditMenu)

# Extensions Menu
ExtensionsMenu = Menu(MenuBar, tearoff=0)
ExtensionsMenu.add_command(label="Load Extension...", command=lambda: load_plugins(app))
ExtensionsMenu.add_command(label="Unload All Extensions", command=lambda: unload_plugins(app, clear_saved=True))
MenuBar.add_cascade(label="Extensions", menu=ExtensionsMenu)
ExtensionsMenu.add_separator()

# Help Menu
HelpMenu = Menu(MenuBar, tearoff=0)
HelpMenu.add_command(label="About PaperClip", command=lambda: showinfo("About PaperClip", "PaperClip by Sparklee"))
MenuBar.add_cascade(label="Help", menu=HelpMenu)

# -------------------- App Instance --------------------
app = AppContext(root, TextArea, ExtensionsMenu, FileMenu)

# Load saved plugins
load_saved_plugins(app)
last_file = load_last_file()
if last_file and os.path.exists(last_file):
    openFile(root, TextArea, update_line_numbers_func, update_statusbar_func, app, path=last_file)

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
