import os
import json
import importlib.util
import sys
from tkinter import filedialog

CONFIG_FILE = "plugins.json"

# ---------------- PluginContext Class ----------------
class PluginContext:
    def __init__(self):
        self.menu_items = []   # store tuples (menu, index)
        self.bindings = []     # store widget bindings

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

def _patch_add_command(menu, context):
    """Patch a menu to track items added by plugins."""
    original_add_command = menu.add_command

    def tracked_add_command(*args, **kwargs):
        index = menu.index("end")
        if index is None:
            index = 0
        else:
            index += 1
        context.menu_items.append((menu, index))
        original_add_command(*args, **kwargs)

    menu.add_command = tracked_add_command
    return original_add_command

def _load_plugin_file(filepath, app):
    plugin_name = os.path.basename(filepath)[:-3]
    spec = importlib.util.spec_from_file_location(plugin_name, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    context = PluginContext()
    plugin_contexts[plugin_name] = context

    if hasattr(module, "on_load"):
        # Patch all main menus of the app to track plugin items
        original_methods = []
        for menu_attr in ["FileMenu", "EditMenu", "ExtensionsMenu", "HelpMenu"]:
            if hasattr(app, menu_attr):
                menu = getattr(app, menu_attr)
                original_methods.append((menu, _patch_add_command(menu, context)))

        # Call plugin
        module.on_load(app, context)

        # Restore original methods
        for menu, original_add in original_methods:
            menu.add_command = original_add

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
                module.on_unload(app)

        # Remove all menu items added by plugin
        if context:
            for item in reversed(context.menu_items):
                if isinstance(item, tuple) and len(item) == 2:
                    menu, index = item
                    try:
                        menu.delete(index)
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
