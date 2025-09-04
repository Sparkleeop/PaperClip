# functions/styling_ops.py
from tkinter import font, TclError, Toplevel, StringVar, IntVar, Label, Button, Spinbox, Text, colorchooser
from tkinter.simpledialog import askstring, askinteger
from tkinter.ttk import Combobox

# ---------------- Font Settings ---------------- #
def set_font(TextArea, app=None):
    """Open a small floating window to choose font family and size with live preview."""
    # Current font
    current_family, current_size = ("Arial", 13)
    if app and hasattr(app, "current_font"):
        current_family, current_size = app.current_font
    else:
        cf = TextArea.cget("font").split()
        current_family = cf[0]
        current_size = int(cf[1])

    # Popup window
    win = Toplevel()
    win.title("Font Settings")
    win.resizable(False, False)

    Label(win, text="Font Family:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    Label(win, text="Font Size:").grid(row=1, column=0, padx=5, pady=5, sticky="w")

    font_var = StringVar(value=current_family)
    size_var = IntVar(value=current_size)

    family_box = Combobox(win, textvariable=font_var, values=sorted(list(font.families())), state="readonly")
    family_box.grid(row=0, column=1, padx=5, pady=5)
    size_box = Spinbox(win, from_=8, to=72, textvariable=size_var, width=5)
    size_box.grid(row=1, column=1, padx=5, pady=5)

    # Preview Text
    preview = Text(win, width=20, height=3)
    preview.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
    preview.insert("1.0", "The quick brown fox jumps over the lazy dog")
    preview.config(state="disabled")

    # Update preview in real-time
    def update_preview(*args):
        new_font = (font_var.get(), size_var.get())
        preview.config(state="normal")
        preview.delete("1.0", "end")
        preview.insert("1.0", "The quick brown fox jumps over the lazy dog")
        preview.config(font=new_font)
        preview.config(state="disabled")
    
    font_var.trace_add("write", update_preview)
    size_var.trace_add("write", update_preview)
    update_preview()

    # Apply to TextArea
    def apply_font():
        new_font = (font_var.get(), size_var.get())
        TextArea.config(font=new_font)
        if app:
            app.current_font = new_font
        win.destroy()

    Button(win, text="Apply", command=apply_font).grid(row=3, column=0, columnspan=2, pady=10)
    win.grab_set()

# ---------------- Basic Styles ---------------- #
def _toggle_style(TextArea, style_tag, style_config, app=None):
    """Helper to toggle a tag on selected text."""
    try:
        start = TextArea.index("sel.first")
        end = TextArea.index("sel.last")
    except TclError:
        return
    if style_tag in TextArea.tag_names("sel.first"):
        TextArea.tag_remove(style_tag, start, end)
    else:
        TextArea.tag_add(style_tag, start, end)
        TextArea.tag_config(style_tag, **style_config)

def toggle_bold(TextArea, app=None):
    family, size = getattr(app, "current_font", ("Arial", 13))
    _toggle_style(TextArea, "bold", {"font": (family, size, "bold")}, app)

def toggle_italic(TextArea, app=None):
    family, size = getattr(app, "current_font", ("Arial", 13))
    _toggle_style(TextArea, "italic", {"font": (family, size, "italic")}, app)

def toggle_underline(TextArea, app=None):
    family, size = getattr(app, "current_font", ("Arial", 13))
    _toggle_style(TextArea, "underline", {"font": (family, size, "underline")}, app)

# ---------------- Headings ---------------- #
def apply_heading(TextArea, level=1, app=None):
    family, size = getattr(app, "current_font", ("Arial", 13))
    sizes = {1: 24, 2: 18, 3: 14}
    _toggle_style(TextArea, f"heading{level}", {"font": (family, sizes[level], "bold")}, app)

# ---------------- Alignment ---------------- #
def set_alignment(TextArea, align):
    # Remove previous alignment tags
    for tag in ["align_left", "align_center", "align_right"]:
        TextArea.tag_remove(tag, "1.0", "end")

    # Configure new alignment
    if align == "left":
        TextArea.tag_configure("align_left", justify="left")
        TextArea.tag_add("align_left", "sel.first", "sel.last")
    elif align == "center":
        TextArea.tag_configure("align_center", justify="center")
        TextArea.tag_add("align_center", "sel.first", "sel.last")
    elif align == "right":
        TextArea.tag_configure("align_right", justify="right")
        TextArea.tag_add("align_right", "sel.first", "sel.last")

# ---------------- Colors ---------------- #
def set_text_color(TextArea):
    try:
        start = TextArea.index("sel.first")
        end = TextArea.index("sel.last")
    except TclError:
        return
    color = colorchooser.askcolor()[1]
    if color:
        tag = f"text_color_{color}"
        TextArea.tag_add(tag, start, end)
        TextArea.tag_config(tag, foreground=color)

def set_highlight_color(TextArea):
    try:
        start = TextArea.index("sel.first")
        end = TextArea.index("sel.last")
    except TclError:
        return
    color = colorchooser.askcolor()[1]
    if color:
        tag = f"highlight_{color}"
        TextArea.tag_add(tag, start, end)
        TextArea.tag_config(tag, background=color)

# ---------------- Clear Formatting ---------------- #
def clear_formatting(TextArea):
    try:
        start = TextArea.index("sel.first")
        end = TextArea.index("sel.last")
    except TclError:
        return
    for tag in TextArea.tag_names():
        TextArea.tag_remove(tag, start, end)

# ---------------- Bullet Formatting ----------------- #
def toggle_bullet(TextArea):
    """Toggle bullets (•) on selected lines or current line."""
    try:
        start = TextArea.index("sel.first linestart")
        end = TextArea.index("sel.last lineend")
    except:
        start = TextArea.index("insert linestart")
        end = TextArea.index("insert lineend")

    lines = TextArea.get(start, end).split("\n")
    new_lines = []

    for line in lines:
        if line.strip().startswith("• "):
            new_lines.append(line.replace("• ", "", 1))
        else:
            new_lines.append("• " + line)

    TextArea.delete(start, end)
    TextArea.insert(start, "\n".join(new_lines))


def toggle_numbered_list(TextArea):
    """Toggle numbered list (1., 2., 3.) on selected lines or current line."""
    try:
        start = TextArea.index("sel.first linestart")
        end = TextArea.index("sel.last lineend")
    except:
        start = TextArea.index("insert linestart")
        end = TextArea.index("insert lineend")

    lines = TextArea.get(start, end).split("\n")
    new_lines = []

    # Check if already numbered
    already_numbered = all(
        line.strip().startswith(f"{i+1}. ") for i, line in enumerate(lines) if line.strip()
    )

    if already_numbered:
        # Remove numbers
        for line in lines:
            if ". " in line:
                new_lines.append(line.split(". ", 1)[1])
            else:
                new_lines.append(line)
    else:
        # Add numbers
        for i, line in enumerate(lines):
            new_lines.append(f"{i+1}. {line}")

    TextArea.delete(start, end)
    TextArea.insert(start, "\n".join(new_lines))


def handle_auto_bullet(event, TextArea):
    """Automatically continue bullets/numbers when Enter is pressed."""
    current_line = TextArea.get("insert linestart", "insert lineend")

    if current_line.strip().startswith("• "):
        TextArea.insert("insert", "\n• ")
        return "break"  # prevent default newline

    elif current_line.strip().startswith("1.") or current_line.strip()[0:2].isdigit():
        try:
            num = int(current_line.strip().split(".")[0])
            TextArea.insert("insert", f"\n{num+1}. ")
            return "break"
        except:
            return None

    return None

