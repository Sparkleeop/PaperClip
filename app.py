import customtkinter as ctk
from tkinter import filedialog, END, Menu

# App setup
ctk.set_appearance_mode("dark")   
ctk.set_default_color_theme("blue")  

app = ctk.CTk()
app.title("*Unsaved - PaperClip by Sparklee")
app.geometry("1200x600")
app.minsize(width=300, height=250)

# Track current file
open_status_name = None

# --- File Functions ---
def new_file():
    global open_status_name
    text.delete("1.0", END)
    app.title("New File - PaperClip by Sparklee")
    status_label.configure(text="New file")
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

    text.delete("1.0", END)
    text.insert(END, content)

    open_status_name = file_path
    app.title(f"{file_path} - PaperClip by Sparklee")
    status_label.configure(text=f"Opened: {file_path}")

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
        f.write(text.get("1.0", "end-1c"))

    open_status_name = file_path
    app.title(f"{file_path} - PaperClip by Sparklee")
    status_label.configure(text=f"Saved: {file_path}")

def save_file():
    global open_status_name
    if open_status_name:
        with open(open_status_name, "w") as f:
            f.write(text.get("1.0", "end-1c"))
        status_label.configure(text=f"Saved: {open_status_name}")
    else:
        saveas_file()

# --- UI Setup ---
# Menu bar (classic Notepad style)
menu_bar = Menu(app)

# File menu
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open...", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As...", command=saveas_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=app.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# You can add Edit/Help menus later if you want
app.config(menu=menu_bar)

# Main frame for textbox
frame = ctk.CTkFrame(app)
frame.pack(pady=5, expand=True, fill="both")

# Textbox with scrollbar
text = ctk.CTkTextbox(
    frame, wrap="word",
    font=("Consolas", 14),
    activate_scrollbars=True
)
text.pack(expand=True, fill="both", padx=10, pady=10)

# Bottom status bar
status_label = ctk.CTkLabel(app, text="Ready", anchor="e")
status_label.pack(fill="x", side="bottom", pady=2)

# Run app
app.mainloop()
