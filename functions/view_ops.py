is_fullscreen = False

def toggle_fullscreen(root, event=None):
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes("-fullscreen", is_fullscreen)

def exit_fullscreen(root, event=None):
    global is_fullscreen
    is_fullscreen = False
    root.attributes("-fullscreen", False)
