from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os
import tkinter.font as tkFont
import importlib
import importlib.util
from tkinter import filedialog, messagebox
import json

plugins = {}
CONFIG_FILE = "plugins.json"


def save_loaded_plugin(filepath):
    try:
        data = []
        if os.path.exists(CONFIG_FILE) and os.path.getsize(CONFIG_FILE) > 0:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
        if filepath not in data:
            data.append(filepath)
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print("Error saving plugin:", e)


def load_saved_plugins(app):
    if os.path.exists(CONFIG_FILE) and os.path.getsize(CONFIG_FILE) > 0:
        with open(CONFIG_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print("Invalid JSON in plugins.json, resetting...")
                data = []
        for filepath in data:
            if os.path.exists(filepath):
                spec = importlib.util.spec_from_file_location(
                    os.path.basename(filepath)[:-3], filepath
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, "on_load"):
                    module.on_load(app)
                plugins[os.path.basename(filepath)[:-3]] = module

def load_plugins(app):
    filepath = filedialog.askopenfilename(
        defaultextension=".py",
        filetypes=[("Python files", "*.py")]
    )
    if not filepath:
        return

    spec = importlib.util.spec_from_file_location(os.path.basename(filepath)[:-3], filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if hasattr(module, "on_load"):
        module.on_load(app)

    plugins[os.path.basename(filepath)[:-3]] = module
    
    save_loaded_plugin(filepath)

def unload_plugins(app):
    for name, module in plugins.items():
        if hasattr(module, "on_unload"):
            module.on_unload(app)
    plugins.clear()

def newFile():
    global file
    root.title("Untitled - PaperClip by Sparklee")
    file = None
    TextArea.delete(1.0, END)
    update_line_numbers()
    update_statusbar()

def openFile():
    global file

    file = askopenfilename(defaultextension = ".txt", filetypes=[("All files", "*.*"), ("Text Documents", "*.txt")])

    if file == "":
        file = None
    else:
        root.title(os.path.basename(file) + "- PaperClip by Sparklee")
        TextArea.delete(1.0, END)

        f = open(file, "r", encoding="utf-8", errors="replace")
        TextArea.insert(1.0,f.read())

        f.close()
        update_line_numbers()
        update_statusbar()

def saveFile():
    global file
    if file == None:
        file = asksaveasfilename(initialfile = "Untitled.txt",defaultextension = ".txt", filetypes=[("All files", "*.*"), ("Text Documents", "*.txt")])

        if file == "":
            file = None

        else:
            #Save it as a New File
            f = open(file, "w")
            f.write(TextArea.get(1.0, END))
            f.close()

            root.title(os.path.basename(file) + " - PaperClip by Sparklee")
    else:
        f = open(file, "w", encoding="utf-8")
        f.write(TextArea.get(1.0, END))
        f.close()

def saveasFile():
    global file
    file = asksaveasfilename(initialfile = "Untitled.txt",defaultextension = ".txt", filetypes=[("All files", "*.*"), ("Text Documents", "*.txt")])

    if file == "":
        file = None

    with open(file, "w", encoding="utf-8") as f:
        f.write(TextArea.get("1.0", "end-1c"))
    root.title(f"{file} - PaperClip by Sparklee")

    f.close()

def quitApp():
    root.destroy()

def cut():
    TextArea.event_generate(("<<Cut>>"))

def copy():
    TextArea.event_generate(("<<Copy>>"))

def paste():
    TextArea.event_generate(("<<Paste>>"))

def about():
    showinfo("About PaperClip", "PaperClip by Sparklee")

def update_statusbar(event=None):
    # Total lines
    total_lines = int(TextArea.index('end-1c').split('.')[0])
    lines_var.set(f"Lines: {total_lines}")

    # Word count
    text = TextArea.get("1.0", "end-1c")
    words = len(text.split())
    words_var.set(f"Words: {words}")

def update_line_numbers(event=None):
    line_numbers.delete("all")

    # Get index of first and last visible line
    first_visible = TextArea.index("@0,0")
    last_visible = TextArea.index("@0,%d" % TextArea.winfo_height())

    # Convert to line numbers
    first_line = int(first_visible.split(".")[0])
    last_line = int(last_visible.split(".")[0])

    # Calculate needed width
    digits = len(str(int(TextArea.index("end-1c").split(".")[0])))
    font = tkFont.Font(font=TextArea["font"])
    new_width = max(30, digits * font.measure("0") + 10)  # add 10px padding
    line_numbers.config(width=new_width)

    # Draw only visible line numbers
    for line in range(first_line, last_line + 1):
        dline = TextArea.dlineinfo(f"{line}.0")
        if dline:
            y = dline[1]  # y-position from dlineinfo
            line_numbers.create_text(new_width - 5, y, anchor="ne", text=str(line), font=TextArea["font"], fill="#858585")


if __name__ == '__main__':

    # Creating an instance of tkinter
    root = Tk()
    # Adding title
    root.title("Untitled - PaperClip by Sparklee")
    # Setting icon
    root.iconbitmap("C:/Users/User 1/OneDrive - Sellability PS/Documents/Sparsh/NotePAD/assets/icon.ico")
    # Setting default size
    root.geometry("1080x720")
    # Setting minimum size
    root.minsize(600, 400)

    # ---------------- Creating a Menu Bar ----------------
    MenuBar = Menu(root)
    root.config(menu = MenuBar)

    # File Menu
    FileMenu = Menu(MenuBar, tearoff = 0)
    # To open a New File
    FileMenu.add_command(label = "New", command = newFile)
    # To open already existing File
    FileMenu.add_command(label = "Open", command = openFile)
    # To save the current file
    FileMenu.add_command(label = "Save", command = saveFile)
    # To save as the current file
    FileMenu.add_command(label = "Save As", command = saveasFile)
    # To add a seperating line
    FileMenu.add_separator()
    # To quit the notepad
    FileMenu.add_command(label = "Exit", command = quitApp)
    FileMenu.add_separator()

    MenuBar.add_cascade(label = "File", menu = FileMenu)

    # Edit Menu
    EditMenu = Menu(MenuBar, tearoff = 0)
    # To give a feature of Cut, Copy, Paste
    EditMenu.add_command(label = "Cut", command = cut)
    EditMenu.add_command(label = "Copy", command = copy)
    EditMenu.add_command(label = "Paste", command = paste)
    MenuBar.add_cascade(label = "Edit", menu = EditMenu)
    EditMenu.add_separator()
    
    # Extensions Menu
    ExtensionsMenu = Menu(MenuBar, tearoff=0)
    ExtensionsMenu.add_command(label="Load Extension...", command=lambda: load_plugins(app))
    MenuBar.add_cascade(label="Extensions", menu=ExtensionsMenu)


    # Help Menu
    HelpMenu = Menu(MenuBar, tearoff = 0)
    HelpMenu.add_command(label = "About PaperClip", command = about)

    MenuBar.add_cascade(label = "Help", menu = HelpMenu)

    # ---------------- Creating a Text Area with Line Numbers ----------------
    editor_frame = Frame(root)
    editor_frame.pack(expand=True, fill=BOTH)

    # Line numbers widget
    line_numbers = Canvas(editor_frame, width=60, background="#252526", highlightthickness=0)
    line_numbers.pack(side=LEFT, fill=Y)


    # Main text area
    TextArea = Text(editor_frame, font="lucida 13", bg="#1e1e1e", fg="#d4d4d4", insertbackground="white")
    TextArea.pack(side=LEFT, expand=True, fill=BOTH)

    # Scrollbar
    scroll = Scrollbar(editor_frame, command=TextArea.yview)
    scroll.pack(side=RIGHT, fill=Y)
    TextArea.config(yscrollcommand=scroll.set)
    # 1) Handlers
    def _on_scrollbar(*args):          # called by scrollbar
        TextArea.yview(*args)          # args are ('moveto','0.5') or ('scroll','1','units')
        update_line_numbers()

    def _on_text_yscroll(first, last): # called by Text widget
        scroll.set(first, last)        # first/last are floats as strings
        root.after_idle(update_line_numbers)

    # 2) Wiring
    scroll.config(command=_on_scrollbar)
    TextArea.config(yscrollcommand=_on_text_yscroll)

    def _on_mousewheel(event):
        TextArea.yview_scroll(int(-event.delta/120), "units")
        update_line_numbers()
        return "break"

    TextArea.bind("<MouseWheel>", _on_mousewheel)


    file = None

    def combined_update(event=None):
        update_line_numbers(event)
        update_statusbar(event)

    TextArea.bind("<KeyRelease>", combined_update)
    TextArea.bind("<MouseWheel>", combined_update)
    TextArea.bind("<Button-1>", combined_update)
    TextArea.bind("<Configure>", combined_update)
    TextArea.bind("<<Change>>", combined_update)
    TextArea.bind("<Expose>", combined_update)



    # Initialize numbers
    update_line_numbers()

    class AppContext:
        def __init__(self, root, text_area, extensions_menu, file_menu):
            self.root = root
            self.TextArea = text_area
            self.ExtensionsMenu = extensions_menu
            self.FileMenu = file_menu

    app = AppContext(root, TextArea, ExtensionsMenu, FileMenu)

    # After creating app
    load_saved_plugins(app)

    ExtensionsMenu.add_command(
        label="Unload All Extensions",
        command=lambda: unload_plugins(app)
    )

    # ---------------- Creating a Bottom Status Bar ----------------
    statusbar = Frame(root, bd=1, relief=SUNKEN, bg="#2d2d30")
    statusbar.pack(side=BOTTOM, fill=X)

    lines_var = StringVar(value="Lines: 1")
    words_var = StringVar(value="Words: 0")

    Label(statusbar, textvariable=words_var, bg="#2d2d30", fg="#d4d4d4").pack(side=LEFT, padx=10)
    Label(statusbar, textvariable=lines_var, bg="#2d2d30", fg="#d4d4d4").pack(side=LEFT, padx=10)
    Label(statusbar, text="UTF-8", bg="#2d2d30", fg="#d4d4d4").pack(side=LEFT, padx=10)
    Label(statusbar, text="Windows(CRLF)", bg="#2d2d30", fg="#d4d4d4").pack(side=LEFT, padx=10)

    # initialize once after labels exist
    update_statusbar()

    root.mainloop()