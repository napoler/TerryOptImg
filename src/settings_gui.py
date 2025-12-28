import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Import ttkthemes for theme support
try:
    from ttkthemes import ThemedStyle
    THEMES_AVAILABLE = True
except ImportError:
    THEMES_AVAILABLE = False

# Ensure we can import ConfigManager
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config_manager import ConfigManager
from utils.language_manager import LanguageManager

class SettingsDialog(tk.Toplevel):
    """
    Settings Dialog Window.
    @spec: FR-008
    """
    def __init__(self, parent, config_manager: ConfigManager, on_save_callback=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.on_save_callback = on_save_callback
        
        # Get scale from parent window
        self.scale = getattr(parent, 'scale', 1.0)
        
        # Initialize language manager
        self.language_manager = LanguageManager()
        saved_language = self.config_manager.get("language", "Chinese") if self.config_manager else "Chinese"
        self.language_manager.set_language(saved_language)
        
        # Set translated title
        self.title(self.language_manager.t("settings_title"))

        # Make modal
        self.transient(parent)
        self.grab_set()

        # Apply themed style if available
        if THEMES_AVAILABLE:
            self.style = ThemedStyle(self)
            # Use the same theme as parent
            if hasattr(parent, 'current_theme'):
                parent_theme = parent.current_theme
                if hasattr(self.style, 'get_themes'):
                    available_themes = self.style.get_themes()
                    if parent_theme in available_themes:
                        self.style.set_theme(parent_theme)
                    elif "arc" in available_themes:
                        self.style.set_theme("arc")
                else:
                    print("Theme loading warning: get_themes method not available in settings")
            else:
                # Default to arc theme
                if hasattr(self.style, 'get_themes'):
                    available_themes = self.style.get_themes()
                    if "arc" in available_themes:
                        self.style.set_theme("arc")
                else:
                    print("Theme loading warning: get_themes method not available in settings")
        else:
            self.style = ttk.Style(self)
        
        # Enhanced font configuration with modern fonts
        base_font_size = max(int(10 * self.scale), 11)
        title_font_size = max(int(12 * self.scale), 13)
        
        # Try to use modern system fonts
        try:
            import platform
            system = platform.system()
            if system == "Windows":
                default_font = "Segoe UI"
            elif system == "Darwin":  # macOS
                default_font = "SF Pro Display"
            else:  # Linux
                default_font = "DejaVu Sans"
        except:
            default_font = "TkDefaultFont"
        
        # Apply bold fonts to all widgets
        self.style.configure('TLabel', font=(default_font, base_font_size, 'bold'))
        self.style.configure('TButton', font=(default_font, base_font_size, 'bold'))
        self.style.configure('TEntry', font=(default_font, base_font_size, 'bold'))
        self.style.configure('TSpinbox', font=(default_font, base_font_size, 'bold'))
        self.style.configure('TCombobox', font=(default_font, base_font_size, 'bold'))
        self.style.configure('TCheckbutton', font=(default_font, base_font_size, 'bold'))
        self.style.configure('TRadiobutton', font=(default_font, base_font_size, 'bold'))
        self.style.configure('TNotebook', font=(default_font, base_font_size, 'bold'))
        self.style.configure('TNotebook.Tab', font=(default_font, base_font_size, 'bold'))
        self.style.configure('TLabelframe', font=(default_font, title_font_size, 'bold'))
        self.style.configure('TLabelframe.Label', font=(default_font, title_font_size, 'bold'))
        
        # Apply modern color scheme
        self._apply_modern_colors()

        # Enhanced layout with modern sizing
        self.geometry("520x500")
        self.resizable(True, True)
        self.minsize(450, 450)

        self._init_ui()
        self._load_values()
        self._detect_dpi()

        # Center window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def _apply_modern_colors(self):
        """Apply simple high contrast colors for settings dialog"""
        try:
            # Simple high contrast colors
            self.colors = {
                'bg_primary': '#ffffff',
                'bg_secondary': '#f8f9fa',
                'text_primary': '#000000',
                'text_secondary': '#333333',
                'accent': '#007bff',
                'accent_hover': '#0056b3',
                'border': '#cccccc'
            }
            
            # Set window background
            self.configure(bg='white')
            
            # Simple style configuration
            self.style.configure('TFrame', background='white')
            self.style.configure('TLabel', background='white', foreground='black')
            self.style.configure('TButton', background='#007bff', foreground='white')
            self.style.configure('TEntry', fieldbackground='white', foreground='black')
            self.style.configure('TCombobox', fieldbackground='white', foreground='black')
            self.style.configure('TSpinbox', fieldbackground='white', foreground='black')
            self.style.configure('TCheckbutton', background='white', foreground='black')
            self.style.configure('TRadiobutton', background='white', foreground='black')
            self.style.configure('TLabelframe', background='white', foreground='black')
            self.style.configure('TLabelframe.Label', background='white', foreground='black')
            self.style.configure('TNotebook', background='white')
            self.style.configure('TNotebook.Tab', background='white', foreground='black')
            
            # Button hover effects
            self.style.map('TButton',
                         background=[('active', '#0056b3')],
                         foreground=[('active', 'white')])
            
            # Tab hover effects
            self.style.map('TNotebook.Tab',
                         background=[('selected', '#f8f9fa')],
                         foreground=[('selected', '#007bff')])
            
        except Exception as e:
            print(f"Color application warning: {e}")
            self.colors = {}

    def _init_ui(self):
        # Premium spacing for modern layout
        p_xl = int(32 * self.scale)   # Extra large padding
        p_lg = int(24 * self.scale)   # Large padding
        p_md = int(16 * self.scale)   # Medium padding
        p_sm = int(8 * self.scale)    # Small padding
        p_xs = int(4 * self.scale)    # Extra small padding

        # Main container with premium background
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Apply background color
        if hasattr(self, 'colors'):
            main_container.configure(style='TFrame')
            self.configure(bg=self.colors.get('bg_primary', '#f5f7fa'))

        # Premium header with enhanced styling
        header_frame = ttk.Frame(main_container, padding=(p_lg, p_md, p_lg, 0))
        header_frame.pack(fill=tk.X)
        
        # Modern title with premium font
        title_font_size = max(int(18 * self.scale), 20)
        subtitle_font_size = max(int(12 * self.scale), 13)
        
        try:
            import platform
            system = platform.system()
            if system == "Windows":
                default_font = "Segoe UI"
            elif system == "Darwin":
                default_font = "SF Pro Display"
            else:
                default_font = "DejaVu Sans"
        except:
            default_font = "TkDefaultFont"
        
        # Title container
        title_container = ttk.Frame(header_frame)
        title_container.pack(fill=tk.X)
        
        # Main title with icon
        title_label = ttk.Label(title_container, 
                               text="⚙️ Settings", 
                               font=(default_font, title_font_size, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        # Subtitle
        subtitle_label = ttk.Label(title_container, 
                                 text="Customize your experience", 
                                 font=(default_font, subtitle_font_size),
                                 foreground=self.colors.get('text_secondary', '#718096') if hasattr(self, 'colors') else '#718096')
        subtitle_label.pack(side=tk.LEFT, padx=(p_sm, 0))

        # Premium notebook with enhanced styling
        notebook_container = ttk.Frame(main_container, padding=p_lg)
        notebook_container.pack(fill=tk.BOTH, expand=True)
        
        self.notebook = ttk.Notebook(notebook_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Enhanced tabs with better padding and styling
        self.tab_general = ttk.Frame(self.notebook, padding=p_lg)
        self.tab_optimization = ttk.Frame(self.notebook, padding=p_lg)
        self.tab_appearance = ttk.Frame(self.notebook, padding=p_lg)

        self.notebook.add(self.tab_general, text=f"🌐 {self._t('general')}")
        self.notebook.add(self.tab_optimization, text=f"⚡ {self._t('optimization')}")
        self.notebook.add(self.tab_appearance, text=f"🎨 {self._t('appearance')}")

        self._build_general_tab()
        self._build_optimization_tab()
        self._build_appearance_tab()

        # Premium button area with enhanced styling
        button_area = ttk.Frame(main_container, padding=(p_lg, p_md, p_lg, p_lg))
        button_area.pack(fill=tk.X)
        
        # Create card background for buttons
        if hasattr(self, 'colors'):
            button_card = tk.Frame(button_area, 
                                 bg=self.colors.get('bg_card', '#ffffff'), 
                                 relief='solid', bd=1)
        else:
            button_card = tk.Frame(button_area, bg='white', relief='solid', bd=1)
        button_card.pack(fill=tk.X)
        
        # Button container with enhanced spacing
        button_container = ttk.Frame(button_card)
        button_container.pack(fill=tk.X, padx=p_md, pady=p_md)
        
        # Left side info
        info_label = ttk.Label(button_container, 
                             text="💡 Changes will be applied after restart",
                             foreground=self.colors.get('text_secondary', '#718096') if hasattr(self, 'colors') else '#718096')
        info_label.pack(side=tk.LEFT)
        
        # Right side buttons
        button_group = ttk.Frame(button_container)
        button_group.pack(side=tk.RIGHT)
        
        # Premium buttons with modern styling
        cancel_btn = ttk.Button(button_group, text=f"❌ {self._t('cancel')}", command=self.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=p_xs)
        
        save_btn = ttk.Button(button_group, text=f"💾 {self._t('save')}", command=self.save)
        save_btn.pack(side=tk.RIGHT, padx=p_xs)
    
    def _t(self, key: str, **kwargs) -> str:
        """Translation helper method"""
        if self.language_manager:
            return self.language_manager.t(key, **kwargs)
        return key  # Fallback to key if no language manager

    def _build_general_tab(self):
        # Enhanced padding
        p_md = int(12 * self.scale)
        p_sm = int(6 * self.scale)
        
        # Configure grid weights for better layout
        self.tab_general.columnconfigure(0, weight=1)
        self.tab_general.columnconfigure(1, weight=2)
        
        # Section: Language Settings
        lang_frame = ttk.LabelFrame(self.tab_general, text="Language Settings", padding=p_md)
        lang_frame.pack(fill=tk.X, pady=(0, p_md))
        
        # Language selection
        ttk.Label(lang_frame, text=self._t("language")).grid(row=0, column=0, sticky=tk.W, padx=p_sm, pady=p_sm)
        self.lang_var = tk.StringVar()
        lang_values = [self.language_manager.t("English"), self.language_manager.t("Chinese")]
        self.lang_cb = ttk.Combobox(lang_frame, textvariable=self.lang_var,
                                   values=lang_values, state="readonly", width=20)
        self.lang_cb.grid(row=0, column=1, sticky=tk.W, padx=p_sm, pady=p_sm)
        
        # Section: Application Settings
        app_frame = ttk.LabelFrame(self.tab_general, text="Application Settings", padding=p_md)
        app_frame.pack(fill=tk.X, pady=(0, p_md))
        
        app_frame.columnconfigure(0, weight=1)
        
        # Updates checkbox
        self.updates_var = tk.BooleanVar()
        ttk.Checkbutton(app_frame, text=self._t("check_updates"),
                       variable=self.updates_var).grid(row=0, column=0, sticky=tk.W, padx=p_sm, pady=p_sm)

    def _build_optimization_tab(self):
        # Enhanced padding
        p_md = int(12 * self.scale)
        p_sm = int(6 * self.scale)
        
        # Section: Default Optimization Settings
        default_frame = ttk.LabelFrame(self.tab_optimization, text="Default Optimization Settings", padding=p_md)
        default_frame.pack(fill=tk.X, pady=(0, p_md))
        
        # Configure grid weights
        default_frame.columnconfigure(0, weight=1)
        default_frame.columnconfigure(1, weight=2)
        
        # Default Quality
        ttk.Label(default_frame, text="Default Quality:").grid(row=0, column=0, sticky=tk.W, padx=p_sm, pady=p_sm)
        quality_frame = ttk.Frame(default_frame)
        quality_frame.grid(row=0, column=1, sticky=tk.W, padx=p_sm, pady=p_sm)
        self.def_quality_var = tk.IntVar()
        ttk.Spinbox(quality_frame, from_=1, to=100, textvariable=self.def_quality_var, width=10).pack(side=tk.LEFT)
        ttk.Label(quality_frame, text="%").pack(side=tk.LEFT, padx=(4, 0))

        # Default Workers
        ttk.Label(default_frame, text="Default Workers:").grid(row=1, column=0, sticky=tk.W, padx=p_sm, pady=p_sm)
        workers_frame = ttk.Frame(default_frame)
        workers_frame.grid(row=1, column=1, sticky=tk.W, padx=p_sm, pady=p_sm)
        self.def_workers_var = tk.IntVar()
        ttk.Spinbox(workers_frame, from_=1, to=32, textvariable=self.def_workers_var, width=10).pack(side=tk.LEFT)
        ttk.Label(workers_frame, text="threads").pack(side=tk.LEFT, padx=(4, 0))

        # Default Format
        ttk.Label(default_frame, text="Default Format:").grid(row=2, column=0, sticky=tk.W, padx=p_sm, pady=p_sm)
        self.def_format_var = tk.StringVar()
        ttk.Combobox(default_frame, textvariable=self.def_format_var,
                     values=["Keep Original", "jpg", "png", "webp"], state="readonly", width=15).grid(row=2, column=1, sticky=tk.W, padx=p_sm, pady=p_sm)
        
        # Section: Advanced Settings
        advanced_frame = ttk.LabelFrame(self.tab_optimization, text="Advanced Settings", padding=p_md)
        advanced_frame.pack(fill=tk.X)
        
        advanced_frame.columnconfigure(0, weight=1)
        
        # Add future advanced settings here
        ttk.Label(advanced_frame, text="More advanced settings coming soon...", 
                 foreground="gray").pack(padx=p_sm, pady=p_sm)

    def _build_appearance_tab(self):
        # Enhanced padding
        p_md = int(12 * self.scale)
        p_sm = int(6 * self.scale)
        
        # Section: Theme Selection
        theme_frame = ttk.LabelFrame(self.tab_appearance, text="Theme Selection", padding=p_md)
        theme_frame.pack(fill=tk.X, pady=(0, p_md))
        
        theme_frame.columnconfigure(0, weight=1)
        theme_frame.columnconfigure(1, weight=2)
        
        # Theme selection
        ttk.Label(theme_frame, text="Theme:").grid(row=0, column=0, sticky=tk.W, padx=p_sm, pady=p_sm)
        
        if THEMES_AVAILABLE and hasattr(self.style, 'get_themes'):
            # Get available themes
            try:
                available_themes = self.style.get_themes()
                # Sort themes and prioritize modern ones
                modern_themes = ['arc', 'breeze', 'equilux', 'adapta', 'yaru', 'ubuntu']
                other_themes = [t for t in available_themes if t not in modern_themes]
                sorted_themes = [t for t in modern_themes if t in available_themes] + sorted(other_themes)
                
                self.theme_var = tk.StringVar()
                self.theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var,
                                              values=sorted_themes, state="readonly", width=20)
                self.theme_combo.grid(row=0, column=1, sticky=tk.W, padx=p_sm, pady=p_sm)
                
                # Bind change event for live preview
                self.theme_combo.bind('<<ComboboxSelected>>', self._preview_theme)
                
                # Preview button
                preview_frame = ttk.Frame(theme_frame)
                preview_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=p_sm, pady=p_sm)
                ttk.Button(preview_frame, text="🎨 Preview Theme", 
                          command=self._preview_current_theme).pack(side=tk.LEFT)
            except Exception as e:
                print(f"Theme loading error: {e}")
                # Fallback to basic themes
                self.theme_var = tk.StringVar()
                ttk.Combobox(theme_frame, textvariable=self.theme_var,
                            values=["System", "Light", "Dark"], state="readonly", width=20).grid(row=0, column=1, sticky=tk.W, padx=p_sm, pady=p_sm)
                ttk.Label(theme_frame, text="(Theme loading error - using basic themes)", 
                         foreground='gray').grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=p_sm, pady=p_sm)
        else:
            # Fallback to basic themes
            self.theme_var = tk.StringVar()
            ttk.Combobox(theme_frame, textvariable=self.theme_var,
                        values=["System", "Light", "Dark"], state="readonly", width=20).grid(row=0, column=1, sticky=tk.W, padx=p_sm, pady=p_sm)
            ttk.Label(theme_frame, text="(Install ttkthemes for more themes)", 
                     foreground='gray').grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=p_sm, pady=p_sm)

        # Section: Display Settings
        display_frame = ttk.LabelFrame(self.tab_appearance, text="Display Settings", padding=p_md)
        display_frame.pack(fill=tk.X, pady=(0, p_md))
        
        display_frame.columnconfigure(0, weight=1)
        display_frame.columnconfigure(1, weight=2)
        
        # UI Scale
        ttk.Label(display_frame, text="UI Scale Factor:").grid(row=0, column=0, sticky=tk.W, padx=p_sm, pady=p_sm)
        scale_container = ttk.Frame(display_frame)
        scale_container.grid(row=0, column=1, sticky=tk.W, padx=p_sm, pady=p_sm)
        self.scale_var = tk.DoubleVar()
        scale_spinbox = ttk.Spinbox(scale_container, from_=0.8, to=2.5, increment=0.1,
                    textvariable=self.scale_var, width=8)
        scale_spinbox.pack(side=tk.LEFT)
        ttk.Label(scale_container, text="(requires restart)").pack(side=tk.LEFT, padx=(4, 0))
        
        # DPI Info
        self.dpi_info_label = ttk.Label(display_frame, text="System DPI: Detecting...")
        self.dpi_info_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=p_sm, pady=p_sm)
        
        # Preset buttons
        preset_label = ttk.Label(display_frame, text="Quick Presets:")
        preset_label.grid(row=2, column=0, sticky=tk.W, padx=p_sm, pady=p_sm)
        
        preset_frame = ttk.Frame(display_frame)
        preset_frame.grid(row=2, column=1, sticky=tk.W, padx=p_sm, pady=p_sm)
        
        ttk.Button(preset_frame, text="100%", command=lambda: self.scale_var.set(1.0)).pack(side=tk.LEFT, padx=2)
        ttk.Button(preset_frame, text="125%", command=lambda: self.scale_var.set(1.25)).pack(side=tk.LEFT, padx=2)
        ttk.Button(preset_frame, text="150%", command=lambda: self.scale_var.set(1.5)).pack(side=tk.LEFT, padx=2)
        ttk.Button(preset_frame, text="175%", command=lambda: self.scale_var.set(1.75)).pack(side=tk.LEFT, padx=2)
        
        # Section: Theme Information
        info_frame = ttk.LabelFrame(self.tab_appearance, text="Theme Information", padding=p_md)
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        # Theme description
        self.theme_desc_label = ttk.Label(info_frame, text="", wraplength=400, justify=tk.LEFT)
        self.theme_desc_label.pack(padx=p_sm, pady=p_sm)

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
        
        # Load theme - handle both ttkthemes and basic themes
        if THEMES_AVAILABLE and hasattr(self.style, 'get_themes'):
            try:
                saved_theme = self.config_manager.get("theme", "arc")
                available_themes = self.style.get_themes()
                if saved_theme in available_themes:
                    self.theme_var.set(saved_theme)
                else:
                    self.theme_var.set("arc")  # Default modern theme
            except Exception as e:
                print(f"Theme loading error in _load_values: {e}")
                self.theme_var.set("System")
        else:
            self.theme_var.set(self.config_manager.get("theme", "System"))
        
        # Update theme description
        self._update_theme_description()
        
        # Detect and display DPI
        self._detect_dpi()

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
    
    def _detect_dpi(self):
        """Detect system DPI and update info label"""
        try:
            # Try to get DPI from parent window
            dpi = self.master.winfo_fpixels('1i')
            auto_scale = max(1.0, dpi / 96.0)
            self.dpi_info_label.config(text=f"System DPI: {dpi:.0f} (Auto: {auto_scale:.1f}x)")
        except Exception:
            try:
                # Fallback for Linux
                import subprocess
                result = subprocess.run(['xdpyinfo'], capture_output=True, text=True, timeout=3)
                for line in result.stdout.split('\n'):
                    if 'resolution' in line.lower():
                        dpi_val = line.split()[-2]
                        dpi = float(dpi_val)
                        auto_scale = max(1.0, dpi / 96.0)
                        self.dpi_info_label.config(text=f"System DPI: {dpi:.0f} (Auto: {auto_scale:.1f}x)")
                        break
                else:
                    self.dpi_info_label.config(text="System DPI: 96 (Auto: 1.0x)")
            except Exception:
                self.dpi_info_label.config(text="System DPI: Unknown (Auto: 1.0x)")
    
    def _preview_theme(self, event=None):
        """Preview selected theme"""
        if THEMES_AVAILABLE and hasattr(self.style, 'get_themes'):
            try:
                selected_theme = self.theme_var.get()
                if selected_theme in self.style.get_themes():
                    self.style.set_theme(selected_theme)
                    self._update_theme_description()
            except Exception as e:
                print(f"Theme preview error: {e}")
    
    def _preview_current_theme(self):
        """Preview currently selected theme"""
        self._preview_theme()
    
    def _update_theme_description(self):
        """Update theme description label"""
        if not hasattr(self, 'theme_desc_label'):
            return
            
        theme_descriptions = {
            'arc': 'Modern, clean theme with rounded corners and subtle shadows. Great for daily use.',
            'breeze': 'KDE-inspired theme with flat design and excellent contrast.',
            'equilux': 'Dark theme with good contrast and reduced eye strain.',
            'adapta': 'Material Design inspired theme with vibrant colors.',
            'yaru': 'Ubuntu\'s default theme - modern and friendly.',
            'ubuntu': 'Classic Ubuntu theme with orange accents.',
            'clearlooks': 'Traditional GTK theme with simple, clean appearance.',
            'radiance': 'Light theme with good visibility and professional look.',
            'elegance': 'Sophisticated theme with subtle gradients and shadows.'
        }
        
        current_theme = self.theme_var.get() if hasattr(self, 'theme_var') else ""
        description = theme_descriptions.get(current_theme, f"Selected theme: {current_theme}")
        
        if not THEMES_AVAILABLE:
            description += "\n\nInstall ttkthemes library for more theme options."
        
        self.theme_desc_label.config(text=description)

if __name__ == "__main__":
    # Test harness
    root = tk.Tk()
    cm = ConfigManager()
    btn = ttk.Button(root, text="Settings", command=lambda: SettingsDialog(root, cm))
    btn.pack(padx=20, pady=20)
    root.mainloop()
