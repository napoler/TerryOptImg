import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import queue
import os
import sys

# Import ttkthemes for modern themes
try:
    from ttkthemes import ThemedStyle
    THEMES_AVAILABLE = True
except ImportError:
    THEMES_AVAILABLE = False
    print("Warning: ttkthemes not available. Using default theme.")

# Ensure src is in path if running from root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import Utils
try:
    from utils.config_manager import ConfigManager
    from utils.language_manager import LanguageManager
except ImportError:
    try:
        from src.utils.config_manager import ConfigManager
        from src.utils.language_manager import LanguageManager
    except ImportError:
        # Fallback if structure is flat or different
        ConfigManager = None
        LanguageManager = None

# Import Settings Dialog
try:
    from settings_gui import SettingsDialog
except ImportError:
    try:
        from src.settings_gui import SettingsDialog
    except ImportError:
        SettingsDialog = None

try:
    from image_optimizer import ImageOptimizer
except ImportError:
    # If running from root without package structure
    try:
        from src.image_optimizer import ImageOptimizer
    except ImportError:
        # If running as script inside src/
        import image_optimizer

class OptimizerApp(tk.Tk):
    """
    Main GUI Application.
    @spec: FR-004 (GUI), FR-005 (Concurrency)
    """
    def __init__(self):
        super().__init__()
        
        # Initialize Config Manager
        if ConfigManager:
            self.config_manager = ConfigManager()
        else:
            self.config_manager = None
            print("Warning: ConfigManager not loaded.")

        # Initialize Language Manager
        if LanguageManager:
            self.language_manager = LanguageManager()
            # Load saved language or default
            saved_language = self.config_manager.get("language", "Chinese") if self.config_manager else "Chinese"
            self.language_manager.set_language(saved_language)
            self.title(self.language_manager.t("app_title"))
        else:
            self.language_manager = None
            print("Warning: LanguageManager not loaded.")
            self.title("TerryOptImg - Image Optimizer")

        # Optimized Scaling with Performance Focus
        try:
            # Primary DPI detection
            dpi = self.winfo_fpixels('1i')
            print(f"Detected DPI: {dpi:.1f}")
        except Exception:
            dpi = 96.0
            print(f"Using fallback DPI: {dpi:.1f}")

        # Load scale from config if available
        user_scale = 1.0
        if self.config_manager:
            user_scale = self.config_manager.get("ui_scale", 1.3)  # Default to 1.3 for better performance

        # Simplified scaling logic - avoid complex calculations
        if user_scale != 1.0:
            self.scale = user_scale
            print(f"Using manual scale: {self.scale:.1f}x")
        else:
            # Simple DPI-based scaling with performance focus
            self.scale = min(max(dpi / 96.0, 1.0), 1.5)  # Cap at 1.5 for performance
            print(f"Using auto-detected scale: {self.scale:.1f}x (DPI: {dpi:.1f})")
        
        # Cache scale value to avoid recalculation
        self._cached_scale = self.scale

        # Set window size with performance considerations
        width = int(600 * self.scale)
        height = int(700 * self.scale)
        self.geometry(f"{width}x{height}")
        
        # Optimize window rendering for better drag performance
        self.resizable(True, True)  # Allow resizing
        
        # Performance optimizations for smooth dragging
        try:
            # Disable expensive visual effects that cause lag
            self.attributes('-alpha', 1.0)  # Ensure full opacity
            self.attributes('-topmost', False)  # Not always on top
            
            # Set window manager hints for better performance
            self.attributes('-toolwindow', False)
            
            # Optimize for smooth resizing
            self.update_idletasks()  # Force immediate update
        except Exception as e:
            print(f"Window optimization warning: {e}")
            pass
        
        # Set minimum size to prevent too small windows
        self.minsize(int(400 * self.scale), int(500 * self.scale))

        # Use basic ttk style for maximum performance
        self.style = ttk.Style(self)
        self.current_theme = "default"
        
        # Apply modern theme if available
        self._apply_modern_theme()
        
        # Minimal font configuration for performance with bold text
        base_font_size = max(int(10 * self.scale), 11)
        
        # Basic font configuration with bold for better visibility
        self.style.configure('TLabel', font=('TkDefaultFont', base_font_size, 'bold'))
        self.style.configure('TButton', font=('TkDefaultFont', base_font_size, 'bold'))
        self.style.configure('TEntry', font=('TkDefaultFont', base_font_size))
        self.style.configure('TSpinbox', font=('TkDefaultFont', base_font_size))
        self.style.configure('TCombobox', font=('TkDefaultFont', base_font_size))
        self.style.configure('TCheckbutton', font=('TkDefaultFont', base_font_size, 'bold'))
        self.style.configure('TRadiobutton', font=('TkDefaultFont', base_font_size, 'bold'))
        
        self.files_to_process = []
        self.processing = False
        self.session_saved_size = 0
        self.queue = queue.Queue()
        self.cancel_event = threading.Event()

        self._init_ui()
        self.load_config()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self._check_queue()

    def _apply_modern_theme(self):
        """Apply modern theme with high contrast colors for visibility"""
        try:
            # Try to use modern themes first
            if THEMES_AVAILABLE:
                available_themes = self.style.theme_names()
                modern_themes = ['arc', 'breeze', 'equilux', 'adapta']
                for theme in modern_themes:
                    if theme in available_themes:
                        self.style.theme_use(theme)
                        self.current_theme = theme
                        break
            
            # Apply high contrast colors
            self.configure(bg='white')
            self.style.configure('TLabel', background='white', foreground='black')
            self.style.configure('TButton', background='#007bff', foreground='white')
            self.style.configure('TEntry', fieldbackground='white', foreground='black')
            self.style.configure('TCombobox', fieldbackground='white', foreground='black')
            self.style.configure('TSpinbox', fieldbackground='white', foreground='black')
            self.style.configure('TCheckbutton', background='white', foreground='black')
            self.style.configure('TRadiobutton', background='white', foreground='black')
            self.style.configure('TLabelframe', background='white', foreground='black')
            self.style.configure('TLabelframe.Label', background='white', foreground='black')
            
        except Exception as e:
            print(f"Theme loading warning: {e}")

    def _init_ui(self):
        # Simple spacing for clean layout
        p_lg = int(20 * self.scale)
        p_md = int(12 * self.scale)
        p_sm = int(8 * self.scale)
        p_xs = int(4 * self.scale)

        # Set window background
        self.configure(bg='white')

        # Main Container
        main_frame = ttk.Frame(self, padding=p_lg)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, p_md))
        
        # Title
        title_font_size = max(int(16 * self.scale), 18)
        title_label = ttk.Label(header_frame, 
                               text="🎨 TerryOptImg - Professional Image Optimizer", 
                               font=('TkDefaultFont', title_font_size, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        # Settings Button
        if SettingsDialog:
            settings_btn = ttk.Button(header_frame, 
                                    text=f"⚙️ {self._t('settings')}", 
                                    command=self.open_settings)
            settings_btn.pack(side=tk.RIGHT, padx=p_xs)

        # File Selection Area
        file_frame = ttk.LabelFrame(main_frame, text=self._t("input_selection"), padding=p_md)
        file_frame.pack(fill=tk.X, pady=p_md)

        self.file_label = ttk.Label(file_frame, text=self._t("no_files_selected"))
        self.file_label.pack(side=tk.LEFT, padx=p_sm)

        btn_frame = ttk.Frame(file_frame)
        btn_frame.pack(side=tk.RIGHT)

        ttk.Button(btn_frame, text=f"📎 {self._t('add_files')}", command=self.select_files).pack(side=tk.LEFT, padx=p_xs)
        ttk.Button(btn_frame, text=f"📂 {self._t('add_folder')}", command=self.select_folder).pack(side=tk.LEFT, padx=p_xs)

        # Settings Area
        settings_frame = ttk.LabelFrame(main_frame, text=self._t("quick_settings"), padding=p_md)
        settings_frame.pack(fill=tk.X, pady=p_md)

        # Grid layout for settings
        # Row 0: Mode & Keep Metadata
        ttk.Label(settings_frame, text=self._t("mode")).grid(row=0, column=0, sticky=tk.W, padx=p_xs, pady=p_sm)
        self.mode_var = tk.StringVar(value="Lossy")
        mode_frame = ttk.Frame(settings_frame)
        mode_frame.grid(row=0, column=1, sticky=tk.W, padx=p_xs, pady=p_sm)
        ttk.Radiobutton(mode_frame, text=self._t("lossy"), variable=self.mode_var, value="Lossy", command=self.toggle_mode).pack(side=tk.LEFT, padx=p_xs)
        ttk.Radiobutton(mode_frame, text=self._t("lossless"), variable=self.mode_var, value="Lossless", command=self.toggle_mode).pack(side=tk.LEFT, padx=p_xs)

        self.keep_metadata_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(settings_frame, text=self._t("keep_metadata"), variable=self.keep_metadata_var).grid(row=0, column=2, sticky=tk.W, padx=p_xs, pady=p_sm)

        # Row 1: Quality & Workers
        ttk.Label(settings_frame, text=self._t("quality")).grid(row=1, column=0, sticky=tk.W, padx=p_xs, pady=p_sm)
        self.quality_var = tk.IntVar(value=85)
        self.quality_spin = ttk.Spinbox(settings_frame, from_=1, to=100, textvariable=self.quality_var, width=5)
        self.quality_spin.grid(row=1, column=1, sticky=tk.W, padx=p_xs, pady=p_sm)

        ttk.Label(settings_frame, text=self._t("workers")).grid(row=1, column=2, sticky=tk.W, padx=p_xs, pady=p_sm)
        self.workers_var = tk.IntVar(value=4)
        ttk.Spinbox(settings_frame, from_=1, to=32, textvariable=self.workers_var, width=5).grid(row=1, column=3, sticky=tk.W, padx=p_xs, pady=p_sm)

        # Row 2: Max Size & Format
        ttk.Label(settings_frame, text=self._t("max_size")).grid(row=2, column=0, sticky=tk.W, padx=p_xs, pady=p_sm)
        self.max_size_var = tk.StringVar(value="")
        ttk.Entry(settings_frame, textvariable=self.max_size_var, width=10).grid(row=2, column=1, sticky=tk.W, padx=p_xs, pady=p_sm)

        ttk.Label(settings_frame, text=self._t("format")).grid(row=2, column=2, sticky=tk.W, padx=p_xs, pady=p_sm)
        self.format_var = tk.StringVar(value="Keep Original")
        format_values = [self._t("keep_original"), "jpg", "png", "webp"]
        ttk.Combobox(settings_frame, textvariable=self.format_var, values=format_values, state="readonly", width=12).grid(row=2, column=3, sticky=tk.W, padx=p_xs, pady=p_sm)

        # Row 3: Output & Overwrite
        self.overwrite_var = tk.BooleanVar(value=False)
        self.overwrite_chk = ttk.Checkbutton(settings_frame, text=self._t("overwrite_input"), variable=self.overwrite_var, command=self.toggle_output)
        self.overwrite_chk.grid(row=3, column=0, columnspan=2, sticky=tk.W, padx=p_xs, pady=p_sm)

        self.output_btn = ttk.Button(settings_frame, text=self._t("select_output"), command=self.select_output)
        self.output_btn.grid(row=3, column=2, sticky=tk.W, padx=p_xs, pady=p_sm)
        self.output_path = None
        self.output_label = ttk.Label(settings_frame, text=self._t("default_output"))
        self.output_label.grid(row=3, column=3, sticky=tk.W, padx=p_xs, pady=p_sm)

        # Progress Area
        progress_frame = ttk.LabelFrame(main_frame, text=self._t("progress"), padding=p_md)
        progress_frame.pack(fill=tk.X, pady=p_md)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=(0, p_sm))

        self.status_label = ttk.Label(progress_frame, text=self._t("ready"))
        self.status_label.pack(anchor=tk.W)

        # Action Button
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=p_md)
        self.start_btn = ttk.Button(btn_frame, text=f"▶ {self._t('start_optimization')}", command=self.start_processing)
        self.start_btn.pack(side=tk.LEFT, padx=p_sm)
        self.stop_btn = ttk.Button(btn_frame, text=f"⏹ {self._t('stop')}", command=self.stop_processing, state="disabled")
        self.stop_btn.pack(side=tk.LEFT, padx=p_sm)

        # Log Area
        log_frame = ttk.LabelFrame(main_frame, text=self._t("log"), padding=p_md)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, p_lg))

        self.log_text = tk.Text(log_frame, height=10, width=50, state="disabled")
        self.log_text.tag_config("error", foreground="red")
        self.log_text.tag_config("success", foreground="green")

        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _t(self, key: str, **kwargs) -> str:
        """Translation helper method"""
        if self.language_manager:
            return self.language_manager.t(key, **kwargs)
        return key  # Fallback to key if no language manager
    
    def select_files(self):
        files = filedialog.askopenfilenames(filetypes=[(self._t("images"), "*.jpg *.jpeg *.png *.webp")])
        if files:
            self.files_to_process.extend(files)
            self.update_file_label()

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            path = Path(folder)
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.webp']:
                self.files_to_process.extend(list(map(str, path.rglob(ext))))
                self.files_to_process.extend(list(map(str, path.rglob(ext.upper()))))
            self.update_file_label()

    def update_file_label(self):
        count = len(self.files_to_process)
        self.file_label.config(text=f"{count} {self._t('files_selected')}")

    def toggle_mode(self):
        if self.mode_var.get() == "Lossless":
            self.quality_var.set(100)
            self.quality_spin.state(['disabled'])
        else:
            self.quality_var.set(85)
            self.quality_spin.state(['!disabled'])

    def toggle_output(self):
        if self.overwrite_var.get():
            self.output_btn.state(['disabled'])
            self.output_label.config(text=self._t("output_overwrite"))
            self.output_path = None
        else:
            self.output_btn.state(['!disabled'])
            default_text = self._t("default_output") if not self.output_path else f"Output: {self.output_path}"
            self.output_label.config(text=default_text)

    def select_output(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_path = folder
            self.output_label.config(text=f"Output: {self.output_path}")

    def log(self, message, tag=None):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n", tag)
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def start_processing(self):
        if not self.files_to_process:
            messagebox.showwarning(self._t("warning"), self._t("no_files_warning"))
            return

        if self.processing:
            return

        self.processing = True
        self.session_saved_size = 0
        self.cancel_event.clear()
        self.start_btn.state(['disabled'])
        self.stop_btn.state(['!disabled'])
        self.progress_var.set(0)
        self.log(self._t("starting_processing"))

        # Gather settings
        try:
            max_size = int(self.max_size_var.get()) if self.max_size_var.get() else None
        except ValueError:
            messagebox.showerror(self._t("error"), self._t("max_size_error"))
            self.processing = False
            self.start_btn.state(['!disabled'])
            self.stop_btn.state(['disabled'])
            return

        fmt = self.format_var.get()
        target_format = None if fmt == self._t("keep_original") else fmt

        # Run in thread
        threading.Thread(target=self.run_optimizer, args=(max_size, target_format)).start()

    def stop_processing(self):
        if self.processing:
            self.cancel_event.set()
            self.log(self._t("stopping"), "error")
            self.stop_btn.state(['disabled'])

    def run_optimizer(self, max_size, target_format):
        optimizer = ImageOptimizer(
            output_dir=self.output_path,
            max_size=max_size,
            target_format=target_format,
            overwrite=self.overwrite_var.get(),
            quality=self.quality_var.get(),
            keep_metadata=self.keep_metadata_var.get()
        )

        total = len(self.files_to_process)
        completed = 0

        with ThreadPoolExecutor(max_workers=self.workers_var.get()) as executor:
            futures = []

            # Submit loop
            for f in self.files_to_process:
                if self.cancel_event.is_set():
                    self.queue.put(("log", ("Cancelled remaining tasks", "error")))
                    break
                futures.append(executor.submit(optimizer.process_file, Path(f)))

            # Result loop
            for future in futures:
                try:
                    result = future.result()
                    # Result is now a dict
                    self.queue.put(("progress", (completed + 1, total)))
                    self.queue.put(("log", result))
                except Exception as e:
                    self.queue.put(("log", (f"Exception: {e}", "error")))

                completed += 1

        self.queue.put(("done", None))

    def _check_queue(self):
        try:
            while True:
                msg_type, data = self.queue.get_nowait()
                if msg_type == "progress":
                    completed, total = data
                    self.progress_var.set((completed / total) * 100)
                    self.status_label.config(text=f"{self._t('processing')} {completed}/{total}")
                elif msg_type == "log":
                    if isinstance(data, dict):
                        # Structured log
                        msg = data.get("message", "")
                        tag = "success" if data.get("success") else "error"
                        if data.get("success"):
                            self.session_saved_size += (data.get("original_size", 0) - data.get("new_size", 0))
                        self.log(msg, tag)
                    elif isinstance(data, tuple):
                        self.log(data[0], data[1])
                    else:
                        self.log(data)
                elif msg_type == "done":
                    self.processing = False
                    self.start_btn.state(['!disabled'])
                    self.stop_btn.state(['disabled'])
                    self.status_label.config(text=self._t("completed") if not self.cancel_event.is_set() else self._t("cancelled"))

                    saved_kb = self.session_saved_size / 1024
                    stats_msg = f"{self._t('total_saved')} {saved_kb:.2f} KB"

                    if not self.cancel_event.is_set():
                        messagebox.showinfo(self._t("done"), f"{self._t('optimization_complete')}\n{stats_msg}")
                    else:
                        messagebox.showinfo(self._t("done"), f"{self._t('optimization_stopped')}\n{stats_msg}")
        except queue.Empty:
            pass
        finally:
            self.after(100, self._check_queue)

    def load_config(self):
        if not self.config_manager:
            return

        # Load values from ConfigManager with safety checks
        try:
            if hasattr(self, 'mode_var'):
                self.mode_var.set(self.config_manager.get("mode", "Lossy"))
            if hasattr(self, 'keep_metadata_var'):
                self.keep_metadata_var.set(self.config_manager.get("keep_metadata", False))
            if hasattr(self, 'quality_var'):
                self.quality_var.set(self.config_manager.get("quality", 85))
            if hasattr(self, 'workers_var'):
                self.workers_var.set(self.config_manager.get("workers", 4))
            if hasattr(self, 'max_size_var'):
                self.max_size_var.set(self.config_manager.get("max_size", ""))
            if hasattr(self, 'format_var'):
                self.format_var.set(self.config_manager.get("format", "Keep Original"))
            if hasattr(self, 'overwrite_var'):
                self.overwrite_var.set(self.config_manager.get("overwrite", False))

            out_dir = self.config_manager.get("output_dir", None)
            if out_dir and hasattr(self, 'output_path'):
                self.output_path = out_dir
                if hasattr(self, 'output_label'):
                    self.output_label.config(text=f"Output: {self.output_path}")

            if hasattr(self, 'toggle_output'):
                self.toggle_output() # Refresh UI state
            if hasattr(self, 'toggle_mode'):
                self.toggle_mode() # Refresh mode state
        except Exception as e:
            print(f"Config loading warning: {e}")

    def save_config(self):
        if not self.config_manager:
            return

        self.config_manager.set("mode", self.mode_var.get())
        self.config_manager.set("keep_metadata", self.keep_metadata_var.get())
        self.config_manager.set("quality", self.quality_var.get())
        self.config_manager.set("workers", self.workers_var.get())
        self.config_manager.set("max_size", self.max_size_var.get())
        self.config_manager.set("format", self.format_var.get())
        self.config_manager.set("overwrite", self.overwrite_var.get())
        self.config_manager.set("output_dir", self.output_path)

        self.config_manager.save()

    def open_settings(self):
        if SettingsDialog and self.config_manager:
            SettingsDialog(self, self.config_manager, on_save_callback=self.on_settings_saved)

    def on_settings_saved(self):
        # Refresh UI with new settings
        self.load_config()

    def on_close(self):
        self.save_config()
        self.destroy()

def set_windows_attributes():
    """Enable High DPI awareness and set AppUserModelID on Windows."""
    if sys.platform == "win32":
        try:
            from ctypes import windll, c_int
            # Enhanced DPI Awareness - try multiple methods
            try:
                # Windows 10/11: Per-Monitor V2 DPI Awareness
                windll.shcore.SetProcessDpiAwarenessContext(-3)  # DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2
            except:
                try:
                    # Windows 8.1+: Per-Monitor DPI Awareness
                    windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
                except:
                    # Windows Vista+: System DPI Awareness
                    windll.user32.SetProcessDPIAware()
            
            # AppUserModelID for Taskbar Grouping and Name
            myappid = 'terryoptimg.image.optimizer.1.1.0'
            windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass

if __name__ == "__main__":
    set_windows_attributes()
    app = OptimizerApp()
    app.mainloop()