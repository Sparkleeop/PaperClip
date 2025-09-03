import os
import json
import importlib.util
import sys
from tkinter import filedialog

CONFIG_FILE = "plugins.json"

# ---------------- PluginContext Class ----------------
class PluginContext:
    def __init__(self):
        self.menu_items = []   # Store menu indices
        self.bindings = []     # Store widget bindings

    def track_binding(self, widget, sequence, func):
        widget.bind(sequence, func)
        self.bindings.append((widget, sequence))

    def unbind_all(self):
        for widget, sequence in self.bindings:
            widget.unbind(sequence)
        self.bindings.clear()

# ---------------- Global Variables ----------------
plugins = {}            # plugin_name -> module
plugin_contexts = {}    # plugin_name -> PluginContext

# ---------------- Plugin Management ----------------
def save_loaded_plugin(filepath):
    try:
        data = []
        if os.path.exists(CONFIG_FILE) and os.path.getsize(CONFIG_FILE) > 0:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
        if filepath not in data:
            data.append(filepath)
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print("Error saving plugin:", e)

def _load_plugin_file(filepath, app):
    plugin_name = os.path.basename(filepath)[:-3]
    spec = importlib.util.spec_from_file_location(plugin_name, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    context = PluginContext()
    plugin_contexts[plugin_name] = context

    if hasattr(module, "on_load"):
        module.on_load(app, context)  # Pass context so plugin can track menu items/bindings

    plugins[plugin_name] = module

def load_plugins(app):
    filepath = filedialog.askopenfilename(defaultextension=".py",
                                          filetypes=[("Python files", "*.py")])
    if not filepath:
        return
    _load_plugin_file(filepath, app)
    save_loaded_plugin(filepath)

def load_saved_plugins(app):
    if os.path.exists(CONFIG_FILE) and os.path.getsize(CONFIG_FILE) > 0:
        with open(CONFIG_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
        for filepath in data:
            if os.path.exists(filepath):
                _load_plugin_file(filepath, app)

def unload_plugins(app, clear_saved=True):
    for plugin_name, module in list(plugins.items()):
        context = plugin_contexts.get(plugin_name)

        # Call plugin's on_unload
        if hasattr(module, "on_unload"):
            try:
                module.on_unload(app, context)
            except TypeError:
                # fallback if plugin only accepts app
                module.on_unload(app)

        # Remove menu items added by plugin
        if context:
            for i in reversed(context.menu_items):
                try:
                    app.FileMenu.delete(i)
                except Exception:
                    pass
            context.unbind_all()

        # Remove module from memory
        if module.__name__ in sys.modules:
            del sys.modules[module.__name__]

    # Clear dictionaries
    plugins.clear()
    plugin_contexts.clear()

    # Clear JSON file
    if clear_saved:
        with open(CONFIG_FILE, "w") as f:
            json.dump([], f)
