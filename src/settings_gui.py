import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Ensure we can import ConfigManager
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config_manager import ConfigManager

class SettingsDialog(tk.Toplevel):
    """
    Settings Dialog Window.
    @spec: FR-008
    """
    def __init__(self, parent, config_manager: ConfigManager, on_save_callback=None):
        super().__init__(parent)
        self.title("Settings")
        self.config_manager = config_manager
        self.on_save_callback = on_save_callback

        # Make modal
        self.transient(parent)
        self.grab_set()

        # Layout
        self.geometry("400x350")
        self.resizable(False, False)

        self._init_ui()
        self._load_values()

        # Center window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def _init_ui(self):
        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tabs
        self.tab_general = ttk.Frame(self.notebook, padding=10)
        self.tab_optimization = ttk.Frame(self.notebook, padding=10)
        self.tab_appearance = ttk.Frame(self.notebook, padding=10)

        self.notebook.add(self.tab_general, text="General")
        self.notebook.add(self.tab_optimization, text="Optimization")
        self.notebook.add(self.tab_appearance, text="Appearance")

        self._build_general_tab()
        self._build_optimization_tab()
        self._build_appearance_tab()

        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Save", command=self.save).pack(side=tk.RIGHT, padx=5)

    def _build_general_tab(self):
        # Language
        ttk.Label(self.tab_general, text="Language:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.lang_var = tk.StringVar()
        lang_cb = ttk.Combobox(self.tab_general, textvariable=self.lang_var,
                               values=["English", "Chinese"], state="readonly")
        lang_cb.grid(row=0, column=1, sticky=tk.W, padx=10)

        # Updates
        self.updates_var = tk.BooleanVar()
        ttk.Checkbutton(self.tab_general, text="Check for updates on startup",
                        variable=self.updates_var).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=10)

    def _build_optimization_tab(self):
        # Default Quality
        ttk.Label(self.tab_optimization, text="Default Quality (0-100):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.def_quality_var = tk.IntVar()
        ttk.Spinbox(self.tab_optimization, from_=1, to=100, textvariable=self.def_quality_var, width=5).grid(row=0, column=1, sticky=tk.W, padx=10)

        # Default Workers
        ttk.Label(self.tab_optimization, text="Default Workers:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.def_workers_var = tk.IntVar()
        ttk.Spinbox(self.tab_optimization, from_=1, to=32, textvariable=self.def_workers_var, width=5).grid(row=1, column=1, sticky=tk.W, padx=10)

        # Default Format
        ttk.Label(self.tab_optimization, text="Default Format:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.def_format_var = tk.StringVar()
        ttk.Combobox(self.tab_optimization, textvariable=self.def_format_var,
                     values=["Keep Original", "jpg", "png", "webp"], state="readonly").grid(row=2, column=1, sticky=tk.W, padx=10)

    def _build_appearance_tab(self):
        # UI Scale
        ttk.Label(self.tab_appearance, text="UI Scale Factor (requires restart):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.scale_var = tk.DoubleVar()
        ttk.Spinbox(self.tab_appearance, from_=0.5, to=3.0, increment=0.1,
                    textvariable=self.scale_var, width=5).grid(row=0, column=1, sticky=tk.W, padx=10)

        # Theme (Placeholder)
        ttk.Label(self.tab_appearance, text="Theme:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.theme_var = tk.StringVar()
        ttk.Combobox(self.tab_appearance, textvariable=self.theme_var,
                     values=["System", "Light", "Dark"], state="readonly").grid(row=1, column=1, sticky=tk.W, padx=10)

    def _load_values(self):
        # General
        self.lang_var.set(self.config_manager.get("language", "English"))
        self.updates_var.set(self.config_manager.get("check_updates", True))

        # Optimization
        self.def_quality_var.set(self.config_manager.get("quality", 85))
        self.def_workers_var.set(self.config_manager.get("workers", 4))
        self.def_format_var.set(self.config_manager.get("format", "Keep Original"))

        # Appearance
        self.scale_var.set(self.config_manager.get("ui_scale", 1.0))
        self.theme_var.set(self.config_manager.get("theme", "System"))

    def save(self):
        # Update config manager
        self.config_manager.set("language", self.lang_var.get())
        self.config_manager.set("check_updates", self.updates_var.get())

        self.config_manager.set("quality", self.def_quality_var.get())
        self.config_manager.set("workers", self.def_workers_var.get())
        self.config_manager.set("format", self.def_format_var.get())

        self.config_manager.set("ui_scale", self.scale_var.get())
        self.config_manager.set("theme", self.theme_var.get())

        # Persist to disk
        self.config_manager.save()

        if self.on_save_callback:
            self.on_save_callback()

        self.destroy()

if __name__ == "__main__":
    # Test harness
    root = tk.Tk()
    cm = ConfigManager()
    btn = ttk.Button(root, text="Settings", command=lambda: SettingsDialog(root, cm))
    btn.pack(padx=20, pady=20)
    root.mainloop()
