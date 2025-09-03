import tkinter.font as tkFont

def update_line_numbers(TextArea, line_numbers, event=None):
    line_numbers.delete("all")
    first_visible = TextArea.index("@0,0")
    last_visible = TextArea.index("@0,%d" % TextArea.winfo_height())

    first_line = int(first_visible.split(".")[0])
    last_line = int(last_visible.split(".")[0])

    digits = len(str(int(TextArea.index("end-1c").split(".")[0])))
    font = tkFont.Font(font=TextArea["font"])
    new_width = max(30, digits * font.measure("0") + 10)
    line_numbers.config(width=new_width)

    for line in range(first_line, last_line + 1):
        dline = TextArea.dlineinfo(f"{line}.0")
        if dline:
            y = dline[1]
            line_numbers.create_text(new_width - 5, y, anchor="ne", text=str(line),
                                     font=TextArea["font"], fill="#858585")
