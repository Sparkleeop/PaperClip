def cut(TextArea):
    TextArea.event_generate("<<Cut>>")

def copy(TextArea):
    TextArea.event_generate("<<Copy>>")

def paste(TextArea):
    TextArea.event_generate("<<Paste>>")

def delete_previous_word(TextArea, event=None):
    cursor_index = TextArea.index("insert")
    prev_word_index = TextArea.search(r"\s\w+$", cursor_index, backwards=True, regexp=True)
    if not prev_word_index:
        prev_word_index = "1.0"
    TextArea.delete(prev_word_index, cursor_index)
    return "break"
