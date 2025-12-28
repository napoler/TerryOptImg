#!/usr/bin/env python3
"""
Qt-based Image Optimizer GUI
Modern, beautiful interface using PyQt5
"""
import sys
import os
import threading
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import queue

# Qt imports
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QPushButton, QProgressBar, 
                            QTextEdit, QGroupBox, QGridLayout, QSpinBox, 
                            QComboBox, QCheckBox, QLineEdit, QFileDialog,
                            QMessageBox, QFrame, QSplitter)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor

# Import existing modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from utils.config_manager import ConfigManager
    from utils.language_manager import LanguageManager
except ImportError:
    try:
        from src.utils.config_manager import ConfigManager
        from src.utils.language_manager import LanguageManager
    except ImportError:
        ConfigManager = None
        LanguageManager = None

try:
    from image_optimizer import ImageOptimizer
except ImportError:
    try:
        from src.image_optimizer import ImageOptimizer
    except ImportError:
        import image_optimizer

try:
    from qt_settings_dialog import QtSettingsDialog
except ImportError:
    try:
        from src.qt_settings_dialog import QtSettingsDialog
    except ImportError:
        QtSettingsDialog = None

try:
    from qt_icons import get_icon, get_qicon, get_button_text, get_status_text, get_status_color
except ImportError:
    try:
        from src.qt_icons import get_icon, get_button_text, get_status_text, get_status_color
    except ImportError:
        # Fallback functions
        def get_icon(name, use_emoji=True, fallback_text=True):
            icons = {
                'folder': '📁', 'file': '📄', 'add_files': '📎', 'add_folder': '📂',
                'settings': '⚙️', 'start': '▶', 'stop': '⏹', 'logo': '🎨',
                'progress': '📊', 'log': '📝', 'ready': '🟢', 'processing': '🔄',
                'completed': '✅', 'error': '❌', 'warning': '⚠️', 'info': 'ℹ️'
            }
            return icons.get(name, f'[{name}]')
        
        def get_button_text(text, icon_name=None, use_emoji=True):
            if icon_name:
                return f'{get_icon(icon_name, use_emoji)} {text}'
            return text
        
        def get_status_text(status, use_emoji=True):
            status_map = {'ready': '就绪', 'processing': '处理中', 'completed': '完成', 'failed': '失败'}
            icon = get_icon(status, use_emoji)
            text = status_map.get(status, status)
            return f'{icon} {text}'
        
        def get_status_color(status):
            colors = {'ready': '#27ae60', 'processing': '#f39c12', 'completed': '#27ae60', 'failed': '#e74c3c'}
            return colors.get(status, '#2c3e50')

class WorkerThread(QThread):
    """Worker thread for image processing"""
    progress_updated = pyqtSignal(int, int)
    log_message = pyqtSignal(str, str)
    finished = pyqtSignal()
    
    def __init__(self, files, optimizer, max_workers):
        super().__init__()
        self.files = files
        self.optimizer = optimizer
        self.max_workers = max_workers
        self.cancelled = False
    
    def cancel(self):
        self.cancelled = True
    
    def run(self):
        total = len(self.files)
        completed = 0
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            
            # Submit all tasks
            for file_path in self.files:
                if self.cancelled:
                    self.log_message.emit("取消剩余任务", "error")
                    break
                futures.append(executor.submit(self.optimizer.process_file, Path(file_path)))
            
            # Process results
            for future in futures:
                if self.cancelled:
                    break
                try:
                    result = future.result()
                    completed += 1
                    self.progress_updated.emit(completed, total)
                    
                    if isinstance(result, dict):
                        msg = result.get("message", "")
                        tag = "success" if result.get("success") else "error"
                        self.log_message.emit(msg, tag)
                    else:
                        self.log_message.emit(str(result), "info")
                except Exception as e:
                    self.log_message.emit(f"异常: {e}", "error")
        
        self.finished.emit()

class ModernImageOptimizer(QMainWindow):
    """Modern Qt-based Image Optimizer"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize managers
        if ConfigManager:
            self.config_manager = ConfigManager()
        else:
            self.config_manager = None
            
        if LanguageManager:
            self.language_manager = LanguageManager()
            saved_language = self.config_manager.get("language", "Chinese") if self.config_manager else "Chinese"
            self.language_manager.set_language(saved_language)
        else:
            self.language_manager = None
        
        # Initialize variables
        self.files_to_process = []
        self.worker_thread = None
        self.session_saved_size = 0
        
        # Setup UI
        self.setup_ui()
        self.setup_style()
        self.load_config()
        
    def setup_ui(self):
        """Setup the main UI"""
        self.setWindowTitle("🎨 TerryOptImg - Professional Image Optimizer")
        self.setGeometry(100, 100, 1400, 1000)
        
        # Set window icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'icon.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Create header
        self.create_header(main_layout)
        
        # Create content area with splitter
        splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(splitter)
        
        # Create top section (file selection + settings)
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        top_layout.setSpacing(20)
        
        # File selection section
        self.create_file_selection(top_layout)
        
        # Settings section
        self.create_settings(top_layout)
        
        splitter.addWidget(top_widget)
        
        # Create bottom section (progress + log)
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.setSpacing(15)
        
        # Progress section
        self.create_progress(bottom_layout)
        
        # Log section
        self.create_log(bottom_layout)
        
        splitter.addWidget(bottom_widget)
        
        # Set splitter sizes
        splitter.setSizes([400, 400])
        
        # Create button bar
        self.create_button_bar(main_layout)
        
    def create_header(self, layout):
        """Create header section"""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Box)
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2980b9);
                border-radius: 10px;
                padding: 15px;
            }
        """)
        
        header_layout = QHBoxLayout(header_frame)
        
        # Logo and Title
        logo_label = QLabel()
        logo_icon = get_qicon("logo")
        if not logo_icon.isNull():
            logo_label.setPixmap(logo_icon.pixmap(32, 32))
        else:
            logo_label.setText("🎨")
            logo_label.setStyleSheet("font-size: 24px;")
        logo_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(logo_label)
        
        title_label = QLabel("TerryOptImg - Professional Image Optimizer")
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Settings button
        settings_btn = QPushButton("设置")
        settings_icon = get_qicon("settings")
        if not settings_icon.isNull():
            settings_btn.setIcon(settings_icon)
            settings_btn.setIconSize(QSize(20, 20))
        settings_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.2);
                color: white;
                border: 2px solid white;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.3);
            }
        """)
        settings_btn.clicked.connect(self.open_settings)
        header_layout.addWidget(settings_btn)
        
        layout.addWidget(header_frame)
        
    def create_file_selection(self, layout):
        """Create file selection section"""
        group = QGroupBox(get_button_text("文件选择", "folder"))
        group.setMinimumWidth(400)
        group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                border: 2px solid #3498db;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px 0 10px;
                background: white;
            }
        """)
        
        group_layout = QVBoxLayout(group)
        group_layout.setSpacing(15)
        group_layout.setContentsMargins(20, 30, 20, 20)
        
        # File count label
        self.file_count_label = QLabel(get_button_text("未选择文件", "file"))
        self.file_count_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #2c3e50;
                padding: 10px;
                background: #ecf0f1;
                border-radius: 8px;
            }
        """)
        group_layout.addWidget(self.file_count_label)
        
        # Button layout
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
# Add files button
        add_files_btn = QPushButton("添加文件")
        files_icon = get_qicon("add_files")
        if not files_icon.isNull():
            add_files_btn.setIcon(files_icon)
            add_files_btn.setIconSize(QSize(24, 24))
        add_files_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2980b9, stop:1 #21618c);
            }
            QPushButton:pressed {
                background: #21618c;
            }
        """)
        add_files_btn.clicked.connect(self.select_files)
        btn_layout.addWidget(add_files_btn)
        
# Add folder button
        add_folder_btn = QPushButton("添加文件夹")
        folder_icon = get_qicon("add_folder")
        if not folder_icon.isNull():
            add_folder_btn.setIcon(folder_icon)
            add_folder_btn.setIconSize(QSize(24, 24))
        add_folder_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #27ae60, stop:1 #229954);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #229954, stop:1 #1e8449);
            }
            QPushButton:pressed {
                background: #1e8449;
            }
        """)
        add_folder_btn.clicked.connect(self.select_folder)
        btn_layout.addWidget(add_folder_btn)
        
        group_layout.addLayout(btn_layout)
        layout.addWidget(group)
        
    def create_settings(self, layout):
        """Create settings section"""
        group = QGroupBox(get_button_text("快速设置", "settings"))
        group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                border: 2px solid #3498db;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px 0 10px;
                background: white;
            }
        """)
        
        group_layout = QGridLayout(group)
        group_layout.setSpacing(15)
        group_layout.setContentsMargins(20, 30, 20, 20)
        
        # Mode selection
        mode_label = QLabel("模式:")
        mode_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        group_layout.addWidget(mode_label, 0, 0)
        
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["有损压缩", "无损压缩"])
        self.mode_combo.setStyleSheet(self.get_combo_style())
        self.mode_combo.currentTextChanged.connect(self.toggle_mode)
        group_layout.addWidget(self.mode_combo, 0, 1)
        
        # Keep metadata
        self.keep_metadata_cb = QCheckBox("保留元数据")
        self.keep_metadata_cb.setStyleSheet(self.get_checkbox_style())
        group_layout.addWidget(self.keep_metadata_cb, 0, 2)
        
        # Quality
        quality_label = QLabel("质量:")
        quality_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        group_layout.addWidget(quality_label, 1, 0)
        
        self.quality_spin = QSpinBox()
        self.quality_spin.setRange(1, 100)
        self.quality_spin.setValue(85)
        self.quality_spin.setStyleSheet(self.get_spinbox_style())
        group_layout.addWidget(self.quality_spin, 1, 1)
        
        # Workers
        workers_label = QLabel("线程数:")
        workers_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        group_layout.addWidget(workers_label, 1, 2)
        
        self.workers_spin = QSpinBox()
        self.workers_spin.setRange(1, 32)
        self.workers_spin.setValue(4)
        self.workers_spin.setStyleSheet(self.get_spinbox_style())
        group_layout.addWidget(self.workers_spin, 1, 3)
        
        # Max size
        max_size_label = QLabel("最大尺寸:")
        max_size_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        group_layout.addWidget(max_size_label, 2, 0)
        
        self.max_size_edit = QLineEdit()
        self.max_size_edit.setPlaceholderText("例如: 1920x1080")
        self.max_size_edit.setStyleSheet(self.get_lineedit_style())
        group_layout.addWidget(self.max_size_edit, 2, 1)
        
        # Format
        format_label = QLabel("格式:")
        format_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        group_layout.addWidget(format_label, 2, 2)
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(["保持原格式", "jpg", "png", "webp"])
        self.format_combo.setStyleSheet(self.get_combo_style())
        group_layout.addWidget(self.format_combo, 2, 3)
        
        # Overwrite
        self.overwrite_cb = QCheckBox("覆盖原文件")
        self.overwrite_cb.setStyleSheet(self.get_checkbox_style())
        self.overwrite_cb.stateChanged.connect(self.toggle_output)
        group_layout.addWidget(self.overwrite_cb, 3, 0, 1, 2)
        
        # Output button
        self.output_btn = QPushButton("选择输出目录")
        output_icon = get_qicon("open")
        if not output_icon.isNull():
            self.output_btn.setIcon(output_icon)
            self.output_btn.setIconSize(QSize(24, 24))
        self.output_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f39c12, stop:1 #e67e22);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e67e22, stop:1 #d35400);
            }
            QPushButton:pressed {
                background: #d35400;
            }
        """)
        self.output_btn.clicked.connect(self.select_output)
        group_layout.addWidget(self.output_btn, 3, 2, 1, 2)
        
        # Output path label
        self.output_label = QLabel("默认: 同目录")
        self.output_label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-style: italic;
                padding: 5px;
            }
        """)
        group_layout.addWidget(self.output_label, 4, 0, 1, 4)
        
        layout.addWidget(group)
        
    def create_progress(self, layout):
        """Create progress section"""
        group = QGroupBox(get_button_text("处理进度", "progress"))
        group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                border: 2px solid #27ae60;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px 0 10px;
                background: white;
            }
        """)
        
        group_layout = QVBoxLayout(group)
        group_layout.setSpacing(15)
        group_layout.setContentsMargins(20, 30, 20, 20)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #27ae60;
                border-radius: 10px;
                text-align: center;
                font-weight: bold;
                font-size: 14px;
                color: white;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #27ae60, stop:1 #229954);
                border-radius: 8px;
            }
        """)
        group_layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel(get_status_text("ready"))
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #27ae60;
                padding: 10px;
                background: #d5f4e6;
                border-radius: 8px;
            }
        """)
        group_layout.addWidget(self.status_label)
        
        layout.addWidget(group)
        
    def create_log(self, layout):
        """Create log section"""
        group = QGroupBox(get_button_text("处理日志", "log"))
        group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                border: 2px solid #34495e;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px 0 10px;
                background: white;
            }
        """)
        
        group_layout = QVBoxLayout(group)
        group_layout.setSpacing(10)
        group_layout.setContentsMargins(20, 30, 20, 20)
        
        # Log text area
        self.log_text = QTextEdit()
        self.log_text.setStyleSheet("""
            QTextEdit {
                background: #2c3e50;
                color: #ecf0f1;
                border: 1px solid #34495e;
                border-radius: 8px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
                padding: 10px;
            }
        """)
        self.log_text.setReadOnly(True)
        group_layout.addWidget(self.log_text)
        
        layout.addWidget(group)
        
    def create_button_bar(self, layout):
        """Create button bar"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        # Start button
        self.start_btn = QPushButton("开始优化")
        start_icon = get_qicon("start")
        if not start_icon.isNull():
            self.start_btn.setIcon(start_icon)
            self.start_btn.setIconSize(QSize(32, 32))
        self.start_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #27ae60, stop:1 #229954);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px 30px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #229954, stop:1 #1e8449);
            }
            QPushButton:pressed {
                background: #1e8449;
            }
            QPushButton:disabled {
                background: #bdc3c7;
                color: #7f8c8d;
            }
        """)
        self.start_btn.clicked.connect(self.start_processing)
        button_layout.addWidget(self.start_btn)
        
        # Stop button
        self.stop_btn = QPushButton("停止")
        stop_icon = get_qicon("stop")
        if not stop_icon.isNull():
            self.stop_btn.setIcon(stop_icon)
            self.stop_btn.setIconSize(QSize(32, 32))
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e74c3c, stop:1 #c0392b);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px 30px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #c0392b, stop:1 #a93226);
            }
            QPushButton:pressed {
                background: #a93226;
            }
            QPushButton:disabled {
                background: #bdc3c7;
                color: #7f8c8d;
            }
        """)
        self.stop_btn.clicked.connect(self.stop_processing)
        self.stop_btn.setEnabled(False)
        button_layout.addWidget(self.stop_btn)
        
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
    def setup_style(self):
        """Setup application style"""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #ecf0f1);
            }
        """)
        
    def get_button_style(self, color, size="normal"):
        """Get button style"""
        if size == "large":
            padding = "15px 30px"
            font_size = "16px"
        else:
            padding = "10px 20px"
            font_size = "14px"
            
        return f"""
            QPushButton {{
                background: {color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: {padding};
                font-size: {font_size};
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {color}, stop:1 {color.replace('8', '6')});
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {color.replace('8', '6')}, stop:1 {color});
            }}
            QPushButton:disabled {{
                background: #bdc3c7;
                color: #7f8c8d;
            }}
        """
        
    def get_combo_style(self):
        """Get combobox style"""
        return """
            QComboBox {
                background: white;
                border: 2px solid #3498db;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                min-width: 120px;
            }
            QComboBox:hover {
                border-color: #2980b9;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #3498db;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background: white;
                border: 2px solid #3498db;
                border-radius: 8px;
                selection-background-color: #3498db;
                selection-color: white;
                padding: 5px;
            }
        """
        
    def get_spinbox_style(self):
        """Get spinbox style"""
        return """
            QSpinBox {
                background: white;
                border: 2px solid #3498db;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                min-width: 80px;
            }
            QSpinBox:hover {
                border-color: #2980b9;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                border: none;
                width: 20px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background: #3498db;
            }
        """
        
    def get_checkbox_style(self):
        """Get checkbox style"""
        return """
            QCheckBox {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #3498db;
                border-radius: 4px;
                background: white;
            }
            QCheckBox::indicator:hover {
                border-color: #2980b9;
            }
            QCheckBox::indicator:checked {
                background: #3498db;
                image: none;
            }
            QCheckBox::indicator:checked::after {
                content: "✓";
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
        """
        
    def get_lineedit_style(self):
        """Get line edit style"""
        return """
            QLineEdit {
                background: white;
                border: 2px solid #3498db;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
            }
            QLineEdit:hover {
                border-color: #2980b9;
            }
            QLineEdit:focus {
                border-color: #2980b9;
                outline: none;
            }
        """

    def select_files(self):
        """Select files for processing"""
        files, _ = QFileDialog.getOpenFileNames(
            self, "选择图片文件", "", 
            "图片文件 (*.jpg *.jpeg *.png *.webp);;所有文件 (*)"
        )
        if files:
            self.files_to_process.extend(files)
            self.update_file_count()
            
    def select_folder(self):
        """Select folder for processing"""
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder:
            path = Path(folder)
            for ext in ['*.jpg', '*.jpeg', '*.png', '*.webp']:
                self.files_to_process.extend(list(map(str, path.rglob(ext))))
                self.files_to_process.extend(list(map(str, path.rglob(ext.upper()))))
            self.update_file_count()
            
    def update_file_count(self):
        """Update file count label"""
        count = len(self.files_to_process)
        self.file_count_label.setText(f"📄 已选择 {count} 个文件")
        
    def toggle_mode(self):
        """Toggle between lossy and lossless mode"""
        is_lossless = self.mode_combo.currentText() == "无损压缩"
        self.quality_spin.setEnabled(not is_lossless)
        if is_lossless:
            self.quality_spin.setValue(100)
        else:
            self.quality_spin.setValue(85)
            
    def toggle_output(self):
        """Toggle output selection"""
        if self.overwrite_cb.isChecked():
            self.output_btn.setEnabled(False)
            self.output_label.setText("📁 直接覆盖原文件")
            self.output_path = None
        else:
            self.output_btn.setEnabled(True)
            if not hasattr(self, 'output_path') or not self.output_path:
                self.output_label.setText("📁 选择输出目录")
                
    def select_output(self):
        """Select output directory"""
        folder = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if folder:
            self.output_path = folder
            self.output_label.setText(f"📁 输出: {folder}")
            
    def start_processing(self):
        """Start image processing"""
        if not self.files_to_process:
            QMessageBox.warning(self, "警告", "请先选择要处理的文件！")
            return
            
        if self.worker_thread and self.worker_thread.isRunning():
            return
            
        # Gather settings
        try:
            max_size = None
            if self.max_size_edit.text().strip():
                size_text = self.max_size_edit.text().strip()
                if 'x' in size_text:
                    width, height = map(int, size_text.split('x'))
                    max_size = f"{width}x{height}"
                    
            fmt = self.format_combo.currentText()
            target_format = None if fmt == "保持原格式" else fmt
            
            # Create optimizer
            optimizer = ImageOptimizer(
                output_dir=getattr(self, 'output_path', None),
                max_size=max_size,
                target_format=target_format,
                overwrite=self.overwrite_cb.isChecked(),
                quality=self.quality_spin.value(),
                keep_metadata=self.keep_metadata_cb.isChecked()
            )
            
            # Start worker thread
            self.worker_thread = WorkerThread(
                self.files_to_process, optimizer, self.workers_spin.value()
            )
            self.worker_thread.progress_updated.connect(self.update_progress)
            self.worker_thread.log_message.connect(self.add_log)
            self.worker_thread.finished.connect(self.processing_finished)
            
            # Update UI
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.progress_bar.setValue(0)
            self.status_label.setText(get_status_text("processing"))
            self.status_label.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    font-weight: bold;
                    color: #f39c12;
                    padding: 10px;
                    background: #fef5e7;
                    border-radius: 8px;
                }
            """)
            
            self.add_log("开始处理图像...", "info")
            self.worker_thread.start()
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"启动处理时出错: {e}")
            
    def stop_processing(self):
        """Stop image processing"""
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.cancel()
            self.add_log("正在停止处理...", "warning")
            
    def update_progress(self, completed, total):
        """Update progress bar"""
        progress = int((completed / total) * 100)
        self.progress_bar.setValue(progress)
        self.status_label.setText(f"🔄 处理中... {completed}/{total}")
        
    def add_log(self, message, tag="info"):
        """Add message to log"""
        # Get current time
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Format message based on tag
        if tag == "error":
            formatted_message = f'<span style="color: {get_status_color("error")}; font-weight: bold;">[{timestamp}] {get_icon("error")} {message}</span>'
        elif tag == "success":
            formatted_message = f'<span style="color: {get_status_color("success")}; font-weight: bold;">[{timestamp}] {get_icon("success")} {message}</span>'
        elif tag == "warning":
            formatted_message = f'<span style="color: {get_status_color("warning")}; font-weight: bold;">[{timestamp}] {get_icon("warning")} {message}</span>'
        else:
            formatted_message = f'<span style="color: {get_status_color("info")}; font-weight: bold;">[{timestamp}] {get_icon("info")} {message}</span>'
            
        self.log_text.append(formatted_message)
        
    def processing_finished(self):
        """Handle processing completion"""
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        if hasattr(self.worker_thread, 'cancelled') and self.worker_thread.cancelled:
            self.status_label.setText(get_status_text("cancelled"))
            self.status_label.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    font-weight: bold;
                    color: #e74c3c;
                    padding: 10px;
                    background: #fadbd8;
                    border-radius: 8px;
                }
            """)
            self.add_log("处理已取消", "warning")
        else:
            self.status_label.setText(get_status_text("completed"))
            self.status_label.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    font-weight: bold;
                    color: #27ae60;
                    padding: 10px;
                    background: #d5f4e6;
                    border-radius: 8px;
                }
            """)
            self.add_log("所有文件处理完成！", "success")
            
            # Show summary
            saved_mb = self.session_saved_size / (1024 * 1024)
            QMessageBox.information(
                self, "处理完成", 
                f"图像优化完成！\n节省空间: {saved_mb:.2f} MB"
            )
            
    def open_settings(self):
        """Open settings dialog"""
        if QtSettingsDialog and self.config_manager:
            dialog = QtSettingsDialog(self, self.config_manager)
            dialog.settings_changed.connect(self.on_settings_changed)
            dialog.exec_()
        else:
            QMessageBox.information(self, "设置", "设置对话框不可用")
            
    def on_settings_changed(self):
        """Handle settings changes"""
        self.load_config()
        QMessageBox.information(self, "设置", "设置已更新，部分更改需要重启应用才能生效。")
        
    def load_config(self):
        """Load configuration"""
        if not self.config_manager:
            return
            
        try:
            # Load mode
            mode = self.config_manager.get("mode", "Lossy")
            self.mode_combo.setCurrentText("无损压缩" if mode == "Lossless" else "有损压缩")
            
            # Load other settings
            self.keep_metadata_cb.setChecked(self.config_manager.get("keep_metadata", False))
            self.quality_spin.setValue(self.config_manager.get("quality", 85))
            self.workers_spin.setValue(self.config_manager.get("workers", 4))
            self.max_size_edit.setText(self.config_manager.get("max_size", ""))
            
            fmt = self.config_manager.get("format", "Keep Original")
            self.format_combo.setCurrentText("jpg" if fmt == "jpg" else "png" if fmt == "png" else "webp" if fmt == "webp" else "保持原格式")
            
            self.overwrite_cb.setChecked(self.config_manager.get("overwrite", False))
            
            output_dir = self.config_manager.get("output_dir", None)
            if output_dir:
                self.output_path = output_dir
                self.output_label.setText(f"📁 输出: {output_dir}")
                
        except Exception as e:
            print(f"Config loading warning: {e}")
            
    def save_config(self):
        """Save configuration"""
        if not self.config_manager:
            return
            
        try:
            # Save settings
            self.config_manager.set("mode", "Lossless" if self.mode_combo.currentText() == "无损压缩" else "Lossy")
            self.config_manager.set("keep_metadata", self.keep_metadata_cb.isChecked())
            self.config_manager.set("quality", self.quality_spin.value())
            self.config_manager.set("workers", self.workers_spin.value())
            self.config_manager.set("max_size", self.max_size_edit.text())
            
            fmt = self.format_combo.currentText()
            self.config_manager.set("format", "jpg" if fmt == "jpg" else "png" if fmt == "png" else "webp" if fmt == "webp" else "Keep Original")
            self.config_manager.set("overwrite", self.overwrite_cb.isChecked())
            self.config_manager.set("output_dir", getattr(self, 'output_path', None))
            
            self.config_manager.save()
        except Exception as e:
            print(f"Config saving warning: {e}")

def main():
    """Main function"""
    app = QApplication(sys.argv)
    app.setApplicationName("TerryOptImg")
    app.setApplicationVersion("2.0")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create main window
    window = ModernImageOptimizer()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
