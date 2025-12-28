import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import queue
import os
import sys

# Ensure src is in path if running from root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import Utils
try:
    from utils.config_manager import ConfigManager
except ImportError:
    try:
        from src.utils.config_manager import ConfigManager
    except ImportError:
        # Fallback if structure is flat or different
        ConfigManager = None

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
        self.title("TerryOptImg - Image Optimizer")

        # Initialize Config Manager
        if ConfigManager:
            self.config_manager = ConfigManager()
        else:
            self.config_manager = None
            print("Warning: ConfigManager not loaded.")

        # Enhanced Dynamic Scaling
        try:
            # Primary DPI detection
            dpi = self.winfo_fpixels('1i')
            print(f"Detected DPI: {dpi:.1f}")
        except Exception:
            # Fallback methods
            try:
                # Try system DPI detection on Linux
                import subprocess
                result = subprocess.run(['xdpyinfo'], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if 'resolution' in line.lower():
                        dpi_val = line.split()[-2]
                        dpi = float(dpi_val)
                        break
                else:
                    dpi = 96.0
            except Exception:
                dpi = 96.0
            print(f"Using fallback DPI: {dpi:.1f}")

        # Load scale from config if available
        user_scale = 1.0
        if self.config_manager:
            user_scale = self.config_manager.get("ui_scale", 1.0)

        # Enhanced scaling logic: user_scale acts as multiplier on auto-detected scale
        auto_scale = max(1.2, dpi / 96.0)  # Increased minimum auto-scale
        if user_scale != 1.0:
            self.scale = user_scale  # Manual override takes precedence
            print(f"Using manual scale: {self.scale:.1f}x")
        else:
            self.scale = auto_scale * 1.25  # Additional 25% boost for readability
            print(f"Using auto-detected scale: {self.scale:.1f}x (DPI: {dpi:.1f})")
        
        # Ensure minimum scale for readability - increased to 1.5
        self.scale = max(self.scale, 1.5)

        width = int(600 * self.scale)
        height = int(700 * self.scale)
        self.geometry(f"{width}x{height}")

        # Apply Enhanced Style
        style = ttk.Style(self)
        
        # Enhanced font scaling with minimum size - increased for better readability
        base_font_size = max(int(12 * self.scale), 14)  # Minimum 14pt
        label_font_size = max(int(11 * self.scale), 13)   # Minimum 13pt for labels
        log_font_size = max(int(10 * self.scale), 12)    # Minimum 12pt for log text
        
        # Configure fonts with better readability
        style.configure('.', font=('Helvetica', base_font_size))
        style.configure('TLabel', font=('Helvetica', label_font_size))
        style.configure('TButton', padding=int(6 * self.scale), font=('Helvetica', base_font_size))
        style.configure('TSpinbox', font=('Helvetica', base_font_size))
        style.configure('TCombobox', font=('Helvetica', base_font_size))
        style.configure('TCheckbutton', font=('Helvetica', base_font_size))
        style.configure('TRadiobutton', font=('Helvetica', base_font_size))
        style.configure('TEntry', font=('Helvetica', base_font_size))
        style.configure('Treeview', font=('Helvetica', log_font_size))  # For file list

        self.files_to_process = []
        self.processing = False
        self.session_saved_size = 0
        self.queue = queue.Queue()
        self.cancel_event = threading.Event()

        self._init_ui()
        self.load_config()
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self._check_queue()

    def _init_ui(self):
        p_lg = int(10 * self.scale)
        p_md = int(5 * self.scale)
        p_sm = int(2 * self.scale)

        # Main Container
        main_frame = ttk.Frame(self, padding=p_lg)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # File Selection Area
        file_frame = ttk.LabelFrame(main_frame, text="Input Selection", padding=p_md)
        file_frame.pack(fill=tk.X, pady=p_md)

        self.file_label = ttk.Label(file_frame, text="No files selected")
        self.file_label.pack(side=tk.LEFT, padx=p_md)

        btn_frame = ttk.Frame(file_frame)
        btn_frame.pack(side=tk.RIGHT)

        ttk.Button(btn_frame, text="Add Files", command=self.select_files).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Add Folder", command=self.select_folder).pack(side=tk.LEFT, padx=2)

        # Settings Button (New)
        if SettingsDialog:
            ttk.Button(main_frame, text="⚙ Settings", command=self.open_settings).pack(anchor=tk.E, padx=5)

        # Settings Area
        settings_frame = ttk.LabelFrame(main_frame, text="Quick Settings", padding="5")
        settings_frame.pack(fill=tk.X, pady=5)

        # Grid layout for settings
        # Row 0: Mode & Keep Metadata
        ttk.Label(settings_frame, text="Mode:").grid(row=0, column=0, sticky=tk.W)
        self.mode_var = tk.StringVar(value="Lossy")
        ttk.Radiobutton(settings_frame, text="Lossy", variable=self.mode_var, value="Lossy", command=self.toggle_mode).grid(row=0, column=1, sticky=tk.W)
        ttk.Radiobutton(settings_frame, text="Lossless", variable=self.mode_var, value="Lossless", command=self.toggle_mode).grid(row=0, column=2, sticky=tk.W)

        self.keep_metadata_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(settings_frame, text="Keep Metadata", variable=self.keep_metadata_var).grid(row=0, column=3, sticky=tk.W, padx=5)

        # Row 1: Quality & Workers
        ttk.Label(settings_frame, text="Quality (0-100):").grid(row=1, column=0, sticky=tk.W)
        self.quality_var = tk.IntVar(value=85)
        self.quality_spin = ttk.Spinbox(settings_frame, from_=1, to=100, textvariable=self.quality_var, width=5)
        self.quality_spin.grid(row=1, column=1, sticky=tk.W, padx=5)

        ttk.Label(settings_frame, text="Workers:").grid(row=1, column=2, sticky=tk.W)
        self.workers_var = tk.IntVar(value=4)
        ttk.Spinbox(settings_frame, from_=1, to=32, textvariable=self.workers_var, width=5).grid(row=1, column=3, sticky=tk.W, padx=5)

        # Row 2: Max Size & Format
        ttk.Label(settings_frame, text="Max Width/Height:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.max_size_var = tk.StringVar(value="")
        ttk.Entry(settings_frame, textvariable=self.max_size_var, width=10).grid(row=2, column=1, sticky=tk.W, padx=5)

        ttk.Label(settings_frame, text="Format:").grid(row=2, column=2, sticky=tk.W, pady=5)
        self.format_var = tk.StringVar(value="Keep Original")
        ttk.Combobox(settings_frame, textvariable=self.format_var, values=["Keep Original", "jpg", "png", "webp"], state="readonly", width=12).grid(row=2, column=3, sticky=tk.W, padx=5)

        # Row 3: Output & Overwrite
        self.overwrite_var = tk.BooleanVar(value=False)
        self.overwrite_chk = ttk.Checkbutton(settings_frame, text="Overwrite Input Files", variable=self.overwrite_var, command=self.toggle_output)
        self.overwrite_chk.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)

        self.output_btn = ttk.Button(settings_frame, text="Select Output Folder", command=self.select_output)
        self.output_btn.grid(row=3, column=2, columnspan=2, sticky=tk.W)
        self.output_path = None
        self.output_label = ttk.Label(settings_frame, text="Default: ./optimized/")
        self.output_label.grid(row=4, column=0, columnspan=4, sticky=tk.W)

        # Progress Area
        progress_frame = ttk.Frame(main_frame, padding="5")
        progress_frame.pack(fill=tk.X, pady=10)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X)

        self.status_label = ttk.Label(progress_frame, text="Ready")
        self.status_label.pack(anchor=tk.W)

        # Action Button
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=5)
        self.start_btn = ttk.Button(btn_frame, text="Start Optimization", command=self.start_processing)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn = ttk.Button(btn_frame, text="Stop", command=self.stop_processing, state="disabled")
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        # Log Area
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True)

        log_font_size = max(int(10 * self.scale), 12)  # Minimum 12pt for log
        self.log_text = tk.Text(log_frame, height=10, width=50, state="disabled", 
                               font=('Helvetica', log_font_size))
        self.log_text.tag_config("error", foreground="red")
        self.log_text.tag_config("success", foreground="green")

        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def select_files(self):
        files = filedialog.askopenfilenames(filetypes=[("Images", "*.jpg *.jpeg *.png *.webp")])
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
        self.file_label.config(text=f"{count} files selected")

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
            self.output_label.config(text="Output: Overwrite Input")
            self.output_path = None
        else:
            self.output_btn.state(['!disabled'])
            self.output_label.config(text=f"Output: {self.output_path if self.output_path else 'Default'}")

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
            messagebox.showwarning("Warning", "No files selected!")
            return

        if self.processing:
            return

        self.processing = True
        self.session_saved_size = 0
        self.cancel_event.clear()
        self.start_btn.state(['disabled'])
        self.stop_btn.state(['!disabled'])
        self.progress_var.set(0)
        self.log("Starting processing...")

        # Gather settings
        try:
            max_size = int(self.max_size_var.get()) if self.max_size_var.get() else None
        except ValueError:
            messagebox.showerror("Error", "Max size must be an integer")
            self.processing = False
            self.start_btn.state(['!disabled'])
            self.stop_btn.state(['disabled'])
            return

        fmt = self.format_var.get()
        target_format = None if fmt == "Keep Original" else fmt

        # Run in thread
        threading.Thread(target=self.run_optimizer, args=(max_size, target_format)).start()

    def stop_processing(self):
        if self.processing:
            self.cancel_event.set()
            self.log("Stopping...", "error")
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
                    self.status_label.config(text=f"Processing: {completed}/{total}")
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
                    self.status_label.config(text="Completed!" if not self.cancel_event.is_set() else "Cancelled!")

                    saved_kb = self.session_saved_size / 1024
                    stats_msg = f"Total Saved: {saved_kb:.2f} KB"

                    if not self.cancel_event.is_set():
                        messagebox.showinfo("Done", f"Optimization Complete!\n{stats_msg}")
                    else:
                        messagebox.showinfo("Cancelled", f"Optimization Stopped.\n{stats_msg}")
        except queue.Empty:
            pass
        finally:
            self.after(100, self._check_queue)

    def load_config(self):
        if not self.config_manager:
            return

        # Load values from ConfigManager
        self.mode_var.set(self.config_manager.get("mode", "Lossy"))
        self.keep_metadata_var.set(self.config_manager.get("keep_metadata", False))
        self.quality_var.set(self.config_manager.get("quality", 85))
        self.workers_var.set(self.config_manager.get("workers", 4))
        self.max_size_var.set(self.config_manager.get("max_size", ""))
        self.format_var.set(self.config_manager.get("format", "Keep Original"))
        self.overwrite_var.set(self.config_manager.get("overwrite", False))

        out_dir = self.config_manager.get("output_dir", None)
        if out_dir:
            self.output_path = out_dir
            self.output_label.config(text=f"Output: {self.output_path}")

        self.toggle_output() # Refresh UI state
        self.toggle_mode() # Refresh mode state

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
        # Notify about restart for scale
        # messagebox.showinfo("Info", "Some settings (like UI Scale) require a restart to take effect.")

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
