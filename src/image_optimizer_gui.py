import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import queue
import os
import sys

# Ensure src is in path if running from root
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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
    def __init__(self):
        super().__init__()
        self.title("SpecKit Image Optimizer (Curtail Replica)")
        self.geometry("600x600")

        self.files_to_process = []
        self.processing = False
        self.queue = queue.Queue()

        self._init_ui()
        self._check_queue()

    def _init_ui(self):
        # Main Container
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # File Selection Area
        file_frame = ttk.LabelFrame(main_frame, text="Input Selection", padding="5")
        file_frame.pack(fill=tk.X, pady=5)

        self.file_label = ttk.Label(file_frame, text="No files selected")
        self.file_label.pack(side=tk.LEFT, padx=5)

        btn_frame = ttk.Frame(file_frame)
        btn_frame.pack(side=tk.RIGHT)

        ttk.Button(btn_frame, text="Add Files", command=self.select_files).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Add Folder", command=self.select_folder).pack(side=tk.LEFT, padx=2)

        # Settings Area
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="5")
        settings_frame.pack(fill=tk.X, pady=5)

        # Grid layout for settings
        # Row 0: Quality & Workers
        ttk.Label(settings_frame, text="Quality (0-100):").grid(row=0, column=0, sticky=tk.W)
        self.quality_var = tk.IntVar(value=85)
        ttk.Spinbox(settings_frame, from_=1, to=100, textvariable=self.quality_var, width=5).grid(row=0, column=1, sticky=tk.W, padx=5)

        ttk.Label(settings_frame, text="Workers:").grid(row=0, column=2, sticky=tk.W)
        self.workers_var = tk.IntVar(value=4)
        ttk.Spinbox(settings_frame, from_=1, to=32, textvariable=self.workers_var, width=5).grid(row=0, column=3, sticky=tk.W, padx=5)

        # Row 1: Max Size & Format
        ttk.Label(settings_frame, text="Max Width/Height:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.max_size_var = tk.StringVar(value="")
        ttk.Entry(settings_frame, textvariable=self.max_size_var, width=10).grid(row=1, column=1, sticky=tk.W, padx=5)

        ttk.Label(settings_frame, text="Format:").grid(row=1, column=2, sticky=tk.W, pady=5)
        self.format_var = tk.StringVar(value="Keep Original")
        ttk.Combobox(settings_frame, textvariable=self.format_var, values=["Keep Original", "jpg", "png", "webp"], state="readonly", width=12).grid(row=1, column=3, sticky=tk.W, padx=5)

        # Row 2: Output & Overwrite
        self.overwrite_var = tk.BooleanVar(value=False)
        self.overwrite_chk = ttk.Checkbutton(settings_frame, text="Overwrite Input Files", variable=self.overwrite_var, command=self.toggle_output)
        self.overwrite_chk.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5)

        self.output_btn = ttk.Button(settings_frame, text="Select Output Folder", command=self.select_output)
        self.output_btn.grid(row=2, column=2, columnspan=2, sticky=tk.W)
        self.output_path = None
        self.output_label = ttk.Label(settings_frame, text="Default: ./optimized/")
        self.output_label.grid(row=3, column=0, columnspan=4, sticky=tk.W)

        # Progress Area
        progress_frame = ttk.Frame(main_frame, padding="5")
        progress_frame.pack(fill=tk.X, pady=10)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X)

        self.status_label = ttk.Label(progress_frame, text="Ready")
        self.status_label.pack(anchor=tk.W)

        # Action Button
        self.start_btn = ttk.Button(main_frame, text="Start Optimization", command=self.start_processing)
        self.start_btn.pack(pady=5)

        # Log Area
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="5")
        log_frame.pack(fill=tk.BOTH, expand=True)

        self.log_text = tk.Text(log_frame, height=10, width=50, state="disabled")
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

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def start_processing(self):
        if not self.files_to_process:
            messagebox.showwarning("Warning", "No files selected!")
            return

        if self.processing:
            return

        self.processing = True
        self.start_btn.state(['disabled'])
        self.progress_var.set(0)
        self.log("Starting processing...")

        # Gather settings
        try:
            max_size = int(self.max_size_var.get()) if self.max_size_var.get() else None
        except ValueError:
            messagebox.showerror("Error", "Max size must be an integer")
            self.processing = False
            self.start_btn.state(['!disabled'])
            return

        fmt = self.format_var.get()
        target_format = None if fmt == "Keep Original" else fmt

        # Run in thread
        threading.Thread(target=self.run_optimizer, args=(max_size, target_format)).start()

    def run_optimizer(self, max_size, target_format):
        optimizer = ImageOptimizer(
            output_dir=self.output_path,
            max_size=max_size,
            target_format=target_format,
            overwrite=self.overwrite_var.get(),
            quality=self.quality_var.get()
        )

        total = len(self.files_to_process)
        completed = 0

        with ThreadPoolExecutor(max_workers=self.workers_var.get()) as executor:
            futures = []
            for f in self.files_to_process:
                futures.append(executor.submit(optimizer.process_file, Path(f)))

            for future in futures:
                result = future.result()
                completed += 1
                self.queue.put(("progress", (completed, total)))
                self.queue.put(("log", result))

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
                    self.log(data)
                elif msg_type == "done":
                    self.processing = False
                    self.start_btn.state(['!disabled'])
                    self.status_label.config(text="Completed!")
                    messagebox.showinfo("Done", "Optimization Complete!")
        except queue.Empty:
            pass
        finally:
            self.after(100, self._check_queue)

if __name__ == "__main__":
    app = OptimizerApp()
    app.mainloop()
