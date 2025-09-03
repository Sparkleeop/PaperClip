def update_statusbar(TextArea, lines_var, words_var, event=None):
    total_lines = int(TextArea.index('end-1c').split('.')[0])
    lines_var.set(f"Lines: {total_lines}")

    text = TextArea.get("1.0", "end-1c")
    words = len(text.split())
    words_var.set(f"Words: {words}")
