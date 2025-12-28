"""
Language manager for internationalization support
"""
import json
import os
from typing import Dict, Any

class LanguageManager:
    """Manages language packs and translations"""
    
    def __init__(self, default_language: str = "English"):
        self.current_language = default_language
        self.translations: Dict[str, Dict[str, str]] = {}
        self.fallback_language = "English"
        self._load_language_packs()
    
    def _load_language_packs(self):
        """Load all available language packs"""
        # Get the directory of this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        lang_dir = os.path.join(current_dir, "locales")
        
        # Built-in translations as fallback
        self._load_builtin_translations()
        
        # Load external language files if they exist
        if os.path.exists(lang_dir):
            for filename in os.listdir(lang_dir):
                if filename.endswith('.json'):
                    lang_code = filename[:-5]  # Remove .json extension
                    filepath = os.path.join(lang_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            self.translations[lang_code] = json.load(f)
                    except Exception as e:
                        print(f"Warning: Could not load language pack {filename}: {e}")
    
    def _load_builtin_translations(self):
        """Load built-in translations"""
        # English (fallback)
        self.translations["English"] = {
            # Main window
            "app_title": "TerryOptImg - Image Optimizer",
            "input_selection": "Input Selection",
            "no_files_selected": "No files selected",
            "add_files": "Add Files",
            "add_folder": "Add Folder",
            "settings": "Settings",
            "quick_settings": "Quick Settings",
            "mode": "Mode:",
            "lossy": "Lossy",
            "lossless": "Lossless",
            "keep_metadata": "Keep Metadata",
            "quality": "Quality (0-100):",
            "workers": "Workers:",
            "max_size": "Max Width/Height:",
            "format": "Format:",
            "keep_original": "Keep Original",
            "overwrite_input": "Overwrite Input Files",
            "select_output": "Select Output Folder",
            "default_output": "Default: ./optimized/",
            "output_overwrite": "Output: Overwrite Input",
            "log": "Log",
            "ready": "Ready",
            "start_optimization": "Start Optimization",
            "stop": "Stop",
            "processing": "Processing:",
            "completed": "Completed!",
            "cancelled": "Cancelled!",
            "starting_processing": "Starting processing...",
            "stopping": "Stopping...",
            "cancelled_remaining": "Cancelled remaining tasks",
            
            # Settings dialog
            "settings_title": "Settings",
            "general": "General",
            "optimization": "Optimization", 
            "appearance": "Appearance",
            "language": "Language:",
            "check_updates": "Check for updates on startup",
            "default_quality": "Default Quality (0-100):",
            "default_workers": "Default Workers:",
            "default_format": "Default Format:",
            "ui_scale": "UI Scale Factor (requires restart):",
            "system_dpi": "System DPI:",
            "auto_scale": "Auto:",
            "quick_presets": "Quick Presets:",
            "theme": "Theme:",
            "preview": "Preview",
            "save": "Save",
            "cancel": "Cancel",
            
            # Messages
            "warning": "Warning",
            "no_files_warning": "No files selected!",
            "error": "Error",
            "max_size_error": "Max size must be an integer",
            "done": "Done",
            "optimization_complete": "Optimization Complete!",
            "total_saved": "Total Saved:",
            "optimization_stopped": "Optimization Stopped.",
            
            # File types
            "images": "Images",
            "files_selected": "files selected"
        }
        
        # Chinese
        self.translations["Chinese"] = {
            # Main window
            "app_title": "TerryOptImg - 图像优化器",
            "input_selection": "输入选择",
            "no_files_selected": "未选择文件",
            "add_files": "添加文件",
            "add_folder": "添加文件夹",
            "settings": "设置",
            "quick_settings": "快速设置",
            "mode": "模式：",
            "lossy": "有损压缩",
            "lossless": "无损压缩",
            "keep_metadata": "保留元数据",
            "quality": "质量 (0-100)：",
            "workers": "工作线程：",
            "max_size": "最大宽度/高度：",
            "format": "格式：",
            "keep_original": "保持原格式",
            "overwrite_input": "覆盖输入文件",
            "select_output": "选择输出文件夹",
            "default_output": "默认：./optimized/",
            "output_overwrite": "输出：覆盖输入文件",
            "log": "日志",
            "ready": "就绪",
            "start_optimization": "开始优化",
            "stop": "停止",
            "processing": "处理中：",
            "completed": "已完成！",
            "cancelled": "已取消！",
            "starting_processing": "开始处理...",
            "stopping": "停止中...",
            "cancelled_remaining": "已取消剩余任务",
            
            # Settings dialog
            "settings_title": "设置",
            "general": "常规",
            "optimization": "优化",
            "appearance": "外观",
            "language": "语言：",
            "check_updates": "启动时检查更新",
            "default_quality": "默认质量 (0-100)：",
            "default_workers": "默认工作线程：",
            "default_format": "默认格式：",
            "ui_scale": "界面缩放比例（需要重启）：",
            "system_dpi": "系统DPI：",
            "auto_scale": "自动：",
            "quick_presets": "快速预设：",
            "theme": "主题：",
            "preview": "预览",
            "save": "保存",
            "cancel": "取消",
            
            # Messages
            "warning": "警告",
            "no_files_warning": "未选择文件！",
            "error": "错误",
            "max_size_error": "最大尺寸必须是整数",
            "done": "完成",
            "optimization_complete": "优化完成！",
            "total_saved": "总共节省：",
            "optimization_stopped": "优化已停止。",
            
            # File types
            "images": "图像",
            "files_selected": "个文件已选择"
        }
    
    def set_language(self, language: str):
        """Set current language"""
        if language in self.translations:
            self.current_language = language
        else:
            print(f"Warning: Language '{language}' not available, using '{self.current_language}'")
    
    def get_language(self) -> str:
        """Get current language"""
        return self.current_language
    
    def get_available_languages(self) -> list:
        """Get list of available languages"""
        return list(self.translations.keys())
    
    def translate(self, key: str, **kwargs) -> str:
        """Translate a text key"""
        # Try current language first
        if self.current_language in self.translations:
            if key in self.translations[self.current_language]:
                text = self.translations[self.current_language][key]
                # Apply string formatting if kwargs provided
                if kwargs:
                    try:
                        text = text.format(**kwargs)
                    except (KeyError, ValueError):
                        pass
                return text
        
        # Fallback to default language
        if (self.fallback_language in self.translations and 
            key in self.translations[self.fallback_language]):
            text = self.translations[self.fallback_language][key]
            if kwargs:
                try:
                    text = text.format(**kwargs)
                except (KeyError, ValueError):
                    pass
            return text
        
        # Return key if no translation found
        return key
    
    def t(self, key: str, **kwargs) -> str:
        """Shorthand for translate"""
        return self.translate(key, **kwargs)