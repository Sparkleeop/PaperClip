# <img src="assets/icon.png" alt="PaperClip Logo" width="50"/> PaperClip

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python\&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Project-Active-success)
![Contributions](https://img.shields.io/badge/Contributions-Welcome-brightgreen)

**PaperClip** is an open-source, dark-mode text editor built with [Tkinter](https://docs.python.org/3/library/tkinter.html).
It’s designed as a lightweight yet powerful alternative to Notepad, featuring plugins, themes, markdown preview, and a modern interface.

---

## ✨ Features

* **File Management**

  * New, Open, Save, Save As
  * Open Recent (with clear history)
  * Exit confirmation for unsaved changes
* **Editor Interface**

  * Line numbers synced with text
  * Smooth scrolling
  * Word & line counter in status bar
  * UTF-8 encoding & line ending display
* **Markdown Support**

  * Live Markdown viewer with one click
* **Editing Tools**

  * Cut, copy, paste, undo, redo
  * Duplicate line (Ctrl+D)
  * Delete previous word (Ctrl+Backspace)
* **Rich Formatting**

  * Font picker
  * Bold, italic, underline
  * Headings (H1–H3)
  * Alignment (left, center, right, justify)
  * Text color & highlight color
  * Bullet & numbered lists
  * Clear formatting option
* **Customization**

  * Dynamic **plugins** (load/unload without restart)
  * Theme support (load/unload & save theme)
* **UI & Experience**

  * Modern dark mode by default
  * Scales correctly on high-DPI Windows displays
  * Fullscreen toggle (F11 / Esc)

---

## 🚀 Getting Started

### Requirements

* Python **3.8+**
* Tkinter (usually included with Python)

### Installation & Run

```bash
git clone https://github.com/Sparkleeop/PaperClip.git
cd PaperClip
python app.py
```

---

## 🧩 Plugins

PaperClip supports dynamic plugins:

* Add new menu items
* Create custom shortcuts
* Modify editor behavior or UI

Plugins can be loaded/unloaded at runtime, and the system ensures cleanup of menus and keybindings.
You can find premade plugins [here](https://github.com/Sparkleeop/PaperClip-Extensions).

Examples:

* Highlight words
* Text transformations
* Utility dialogs

---

## 🎨 Themes

PaperClip includes a theme system:

* Load custom `.json` theme files
* Unload/reset to default
* Saved theme auto-loads on next startup

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a feature branch
3. Submit a PR with clear commit messages

---

## 📜 License

PaperClip – Personal Use License

Copyright (c) 2025 Sparklee

You may:

* Use PaperClip on your devices
* Modify the code for personal use

You may **not**:

* Redistribute or sell PaperClip
* Use it commercially without permission

---

## 👤 Author

Developed by **Sparklee**