from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import END
import os

file = None

def newFile(root, TextArea, update_line_numbers, update_statusbar):
    global file
    root.title("Untitled - PaperClip by Sparklee")
    file = None
    TextArea.delete(1.0, END)
    update_line_numbers()
    update_statusbar()

def openFile(root, TextArea, update_line_numbers, update_statusbar):
    global file
    file = askopenfilename(defaultextension=".txt", filetypes=[("All files", "*.*"), ("Text Documents", "*.txt")])
    if not file:
        file = None
        return

    root.title(os.path.basename(file) + " - PaperClip by Sparklee")
    TextArea.delete(1.0, END)
    with open(file, "r", encoding="utf-8", errors="replace") as f:
        TextArea.insert(1.0, f.read())

    update_line_numbers()
    update_statusbar()

def saveFile(root, TextArea):
    global file
    if file is None:
        return saveasFile(root, TextArea)
    
    with open(file, "w", encoding="utf-8") as f:
        f.write(TextArea.get(1.0, END))
    root.title(os.path.basename(file) + " - PaperClip by Sparklee")

def saveasFile(root, TextArea):
    global file
    file = asksaveasfilename(initialfile="Untitled.txt", defaultextension=".txt",
                             filetypes=[("All files", "*.*"), ("Text Documents", "*.txt")])
    if not file:
        return
    with open(file, "w", encoding="utf-8") as f:
        f.write(TextArea.get("1.0", "end-1c"))
    root.title(f"{file} - PaperClip by Sparklee")

def quitApp(root):
    root.destroy()
