# functions/markdown_viewer.py
import tkinter as tk
from tkinter import Toplevel, messagebox
import os

# Try to use tkinterweb (preferred)
try:
    from tkinterweb import HtmlFrame
    _HAS_TKINTERWEB = True
except Exception:
    _HAS_TKINTERWEB = False

# Markdown converter
try:
    import markdown
except Exception:
    markdown = None

# Simple dark-ish styling to match your editor
_CSS = """
<style>
  body{font-family: -apple-system, Segoe UI, Arial, sans-serif; padding:16px; color:#d4d4d4;background:#1e1e1e;}
  h1,h2,h3,h4{color:#ffffff}
  code, pre{background:#2d2d30; padding: 2px 4px; border-radius: 4px;}
  pre{padding: 10px; overflow:auto;}
  table{border-collapse: collapse; margin: 8px 0;}
  td, th{border:1px solid #444; padding: 6px 8px;}
  a{color:#4ea1ff; text-decoration:none}
</style>
"""

def _render_html(md_text: str) -> str:
    html = markdown.markdown(md_text, extensions=["fenced_code", "tables"])
    return f"<html><head>{_CSS}</head><body>{html}</body></html>"

def open_markdown_viewer(root: tk.Tk, text_widget: tk.Text, file_path: str = None):
    """
    Open a live Markdown preview window.
    If tkinterweb is unavailable, falls back to opening a temp HTML in the system browser.
    """
    if markdown is None:
        messagebox.showerror(
            "Missing dependency",
            "The 'markdown' package is required.\nInstall it with:\n\npip install markdown"
        )
        return

    # Fallback: open in default browser (no live updates)
    if not _HAS_TKINTERWEB:
        import tempfile, os, webbrowser
        doc = _render_html(text_widget.get("1.0", "end-1c"))
        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".html", encoding="utf-8") as f:
            f.write(doc)
            tmp_path = os.path.abspath(f.name)
        webbrowser.open(f"file:///{tmp_path}")
        return

    # Preferred: tkinterweb live preview
    win = Toplevel(root)
    if file_path:
        win.title(f"Preview - {os.path.basename(file_path)}")
    else:
        win.title("Preview")
    win.geometry("900x700")

    frame = HtmlFrame(win)
    frame.pack(fill="both", expand=True)

    def render():
        md = text_widget.get("1.0", "end-1c")
        frame.load_html(_render_html(md))

    # Initial render
    render()

    # Live updates — IMPORTANT: DO NOT touch edit_modified flag here,
    # and use add="+" so we don't clobber your existing bindings.
    def on_modified(event=None):
        if not win.winfo_exists():
            return
        root.after_idle(render)

    text_widget.bind("<<Modified>>", on_modified, add="+")
    win.focus_set()
    return win
