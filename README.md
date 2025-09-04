# <img src="assets/icon.png" alt="PaperClip Logo" width="50"/> PaperClip

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python\&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Project-Active-success)
![Contributions](https://img.shields.io/badge/Contributions-Welcome-brightgreen)

PaperClip is an open-source, dark mode text editor built with [Tkinter](https://docs.python.org/3/library/tkinter.html). It is designed to be a lightweight, minimal alternative to traditional text editors like Notepad, providing essential editing features with a modern interface.

---

## Features

* **File Operations:** Create, open, save, and save as text files with UTF-8 encoding
* **Editor Interface:** Line numbers, smooth scrolling, and synced line numbers
* **Dark Mode UI:** Modern and clean interface optimized for extended usage
* **Edit Operations:** Cut, copy, paste, and standard keyboard shortcuts
* **Status Bar:** Displays line and word count, encoding, and line ending type
* **Extensibility:** Load and unload plugins/extensions dynamically for custom features

---

## Getting Started

### Requirements

* Python **3.8+**
* Tkinter (usually pre-installed with Python)

### Installation and Running

```bash
git clone https://github.com/Sparkleeop/PaperClip.git
cd PaperClip
python paperclip.py
```

---

## Plugin/Extension System

PaperClip supports dynamic plugins to extend functionality. Plugins can:

* Add new menu items
* Create keyboard shortcuts
* Modify the editor interface or behavior

Plugins are loaded at runtime and can be unloaded without restarting the application. The plugin system tracks menu items and keybindings for proper cleanup.

You can find premade plugin [here](https://github.com/Sparkleeop/PaperClip-Extensions)

Example plugin features include:

* Highlighting specific words in the editor
* Adding custom text transformations
* Adding utility dialogs

---

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

Please follow standard Git workflow and provide descriptive commit messages.

---

## License

PaperClip – Personal Use License

Copyright (c) 2025 Sparklee

You are granted permission to:
- Use PaperClip on your personal devices.
- Modify the code for personal use.

You MAY NOT:
- Redistribute PaperClip, modified or unmodified, to others.
- Sell, sublicense, or use PaperClip commercially without explicit permission.

All rights not explicitly granted are reserved.

---

## Author

Developed by **Sparklee**
