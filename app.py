import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.title("*Unsaved - PaperClip by Sparklee")
root.iconbitmap("assets/paperclip.ico")
root.geometry("1200x600")
root.minsize(width=300, height=200)

# Track current file name
open_status_name = None

# --- File functions ---

def new_file():
    global open_status_name
    text.delete("1.0", tk.END)
    root.title("New File - PaperClip by Sparklee")
    status_bar.config(text="New file")
    open_status_name = None

def open_file():
    global open_status_name
    file_path = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py")],
        title="Open File"
    )
    if not file_path:
        return
    
    with open(file_path, "r") as f:
        content = f.read()

    text.delete("1.0", tk.END)
    text.insert(tk.END, content)

    open_status_name = file_path
    root.title(f"{file_path} - PaperClip by Sparklee")
    status_bar.config(text=f"Opened: {file_path}")

def saveas_file():
    global open_status_name
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")],
        title="Save File"
    )
    if not file_path:
        return
    
    with open(file_path, "w") as f:
        content = text.get("1.0", "end-1c")
        f.write(content)

    open_status_name = file_path
    root.title(f"{file_path} - PaperClip by Sparklee")
    status_bar.config(text=f"Saved: {file_path}")

def save_file():
    global open_status_name
    if open_status_name:
        with open(open_status_name, "w") as f:
            content = text.get("1.0", "end-1c")
            f.write(content)
        status_bar.config(text=f"Saved: {open_status_name}")
    else:
        saveas_file()


# --- UI setup ---

frame = tk.Frame(root)
frame.pack(pady=5, expand=True, fill="both")

# Scrollbar + Text
text_scroll = tk.Scrollbar(frame)
text_scroll.pack(side="right", fill="y")

text = tk.Text(
    frame, width=97, height=25, font=("Helvetica", 16),
    selectbackground="yellow", selectforeground="black",
    undo=True, yscrollcommand=text_scroll.set
)
text.pack(expand=True, fill="both")
text_scroll.config(command=text.yview)

# Menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=saveas_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.destroy)

# Edit menu (no functionality yet)
edit_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Copy")
edit_menu.add_command(label="Cut")
edit_menu.add_command(label="Paste")
edit_menu.add_command(label="Undo")
edit_menu.add_command(label="Redo")

# Status bar
status_bar = tk.Label(root, text="Ready", anchor="e")
status_bar.pack(fill="x", side="bottom", ipady=5)

root.mainloop()
