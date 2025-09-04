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
