#!/usr/bin/env python3
"""
Qt-based Settings Dialog
Modern settings interface using PyQt5
"""
import sys
import os
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, 
                            QWidget, QLabel, QPushButton, QSpinBox, QComboBox, 
                            QCheckBox, QSlider, QGroupBox, QGridLayout, 
                            QLineEdit, QTextEdit, QFileDialog, QMessageBox,
                            QFormLayout, QFrame, QButtonGroup, QRadioButton)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor

class QtSettingsDialog(QDialog):
    """Modern Qt-based Settings Dialog"""
    
    settings_changed = pyqtSignal()
    
    def __init__(self, parent=None, config_manager=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.setWindowTitle("⚙️ 设置")
        self.setGeometry(200, 200, 900, 700)
        self.setModal(True)
        
        self.setup_ui()
        self.setup_style()
        self.load_settings()
        
    def setup_ui(self):
        """Setup the settings UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Create header
        self.create_header(layout)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #3498db;
                border-radius: 10px;
                background: white;
            }
            QTabBar::tab {
                background: #ecf0f1;
                color: #2c3e50;
                padding: 12px 24px;
                margin-right: 5px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                font-weight: bold;
                font-size: 14px;
            }
            QTabBar::tab:selected {
                background: #3498db;
                color: white;
            }
            QTabBar::tab:hover {
                background: #d5dbdd;
            }
            QTabBar::tab:selected:hover {
                background: #2980b9;
            }
        """)
        
        # Create tabs
        self.create_general_tab()
        self.create_optimization_tab()
        self.create_appearance_tab()
        self.create_advanced_tab()
        
        layout.addWidget(self.tab_widget)
        
        # Create button bar
        self.create_button_bar(layout)
        
    def create_header(self, layout):
        """Create header section"""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Box)
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #9b59b6, stop:1 #8e44ad);
                border-radius: 10px;
                padding: 15px;
            }
        """)
        
        header_layout = QHBoxLayout(header_frame)
        
        # Title
        title_label = QLabel("⚙️ 应用设置")
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        layout.addWidget(header_frame)
        
    def create_general_tab(self):
        """Create general settings tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Language section
        lang_group = QGroupBox("🌐 语言设置")
        lang_group.setStyleSheet(self.get_group_style())
        lang_layout = QFormLayout(lang_group)
        lang_layout.setSpacing(15)
        
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["中文", "English"])
        self.lang_combo.setStyleSheet(self.get_combo_style())
        lang_layout.addRow("界面语言:", self.lang_combo)
        
        layout.addWidget(lang_group)
        
        # Updates section
        updates_group = QGroupBox("🔄 更新设置")
        updates_group.setStyleSheet(self.get_group_style())
        updates_layout = QVBoxLayout(updates_group)
        updates_layout.setSpacing(15)
        
        self.check_updates_cb = QCheckBox("启动时检查更新")
        self.check_updates_cb.setStyleSheet(self.get_checkbox_style())
        updates_layout.addWidget(self.check_updates_cb)
        
        self.auto_updates_cb = QCheckBox("自动下载更新")
        self.auto_updates_cb.setStyleSheet(self.get_checkbox_style())
        updates_layout.addWidget(self.auto_updates_cb)
        
        layout.addWidget(updates_group)
        
        # File associations
        assoc_group = QGroupBox("📁 文件关联")
        assoc_group.setStyleSheet(self.get_group_style())
        assoc_layout = QVBoxLayout(assoc_group)
        assoc_layout.setSpacing(15)
        
        self.associate_cb = QCheckBox("关联常见图片格式")
        self.associate_cb.setStyleSheet(self.get_checkbox_style())
        assoc_layout.addWidget(self.associate_cb)
        
        assoc_info = QLabel("关联后可以通过双击图片文件直接打开优化器")
        assoc_info.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-style: italic;
                padding: 10px;
                background: #f8f9fa;
                border-radius: 5px;
            }
        """)
        assoc_layout.addWidget(assoc_info)
        
        layout.addWidget(assoc_group)
        
        layout.addStretch()
        
        self.tab_widget.addTab(tab, "📋 常规")
        
    def create_optimization_tab(self):
        """Create optimization settings tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Default quality
        quality_group = QGroupBox("🎯 默认质量设置")
        quality_group.setStyleSheet(self.get_group_style())
        quality_layout = QFormLayout(quality_group)
        quality_layout.setSpacing(15)
        
        self.default_quality_spin = QSpinBox()
        self.default_quality_spin.setRange(1, 100)
        self.default_quality_spin.setValue(85)
        self.default_quality_spin.setStyleSheet(self.get_spinbox_style())
        quality_layout.addRow("默认质量 (1-100):", self.default_quality_spin)
        
        self.lossless_quality_spin = QSpinBox()
        self.lossless_quality_spin.setRange(1, 100)
        self.lossless_quality_spin.setValue(100)
        self.lossless_quality_spin.setStyleSheet(self.get_spinbox_style())
        quality_layout.addRow("无损质量 (1-100):", self.lossless_quality_spin)
        
        layout.addWidget(quality_group)
        
        # Performance
        perf_group = QGroupBox("⚡ 性能设置")
        perf_group.setStyleSheet(self.get_group_style())
        perf_layout = QFormLayout(perf_group)
        perf_layout.setSpacing(15)
        
        self.default_workers_spin = QSpinBox()
        self.default_workers_spin.setRange(1, 32)
        self.default_workers_spin.setValue(4)
        self.default_workers_spin.setStyleSheet(self.get_spinbox_style())
        perf_layout.addRow("默认线程数:", self.default_workers_spin)
        
        self.memory_limit_spin = QSpinBox()
        self.memory_limit_spin.setRange(128, 8192)
        self.memory_limit_spin.setValue(1024)
        self.memory_limit_spin.setSuffix(" MB")
        self.memory_limit_spin.setStyleSheet(self.get_spinbox_style())
        perf_layout.addRow("内存限制:", self.memory_limit_spin)
        
        layout.addWidget(perf_group)
        
        # Default format
        format_group = QGroupBox("🖼️ 默认格式")
        format_group.setStyleSheet(self.get_group_style())
        format_layout = QFormLayout(format_group)
        format_layout.setSpacing(15)
        
        self.default_format_combo = QComboBox()
        self.default_format_combo.addItems(["保持原格式", "jpg", "png", "webp"])
        self.default_format_combo.setStyleSheet(self.get_combo_style())
        format_layout.addRow("默认输出格式:", self.default_format_combo)
        
        self.fallback_format_combo = QComboBox()
        self.fallback_format_combo.addItems(["jpg", "png", "webp"])
        self.fallback_format_combo.setStyleSheet(self.get_combo_style())
        format_layout.addRow("后备格式:", self.fallback_format_combo)
        
        layout.addWidget(format_group)
        
        layout.addStretch()
        
        self.tab_widget.addTab(tab, "⚙️ 优化")
        
    def create_appearance_tab(self):
        """Create appearance settings tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Theme
        theme_group = QGroupBox("🎨 主题设置")
        theme_group.setStyleSheet(self.get_group_style())
        theme_layout = QFormLayout(theme_group)
        theme_layout.setSpacing(15)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["现代蓝色", "深色主题", "浅色主题", "高对比度"])
        self.theme_combo.setStyleSheet(self.get_combo_style())
        theme_layout.addRow("界面主题:", self.theme_combo)
        
        # UI Scale
        scale_layout = QHBoxLayout()
        self.scale_slider = QSlider(Qt.Horizontal)
        self.scale_slider.setRange(50, 200)
        self.scale_slider.setValue(100)
        self.scale_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #ecf0f1;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #3498db;
                width: 20px;
                height: 20px;
                border-radius: 10px;
                margin: -6px 0;
            }
            QSlider::handle:horizontal:hover {
                background: #2980b9;
            }
        """)
        self.scale_label = QLabel("100%")
        self.scale_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        self.scale_slider.valueChanged.connect(lambda v: self.scale_label.setText(f"{v}%"))
        
        scale_layout.addWidget(self.scale_slider)
        scale_layout.addWidget(self.scale_label)
        theme_layout.addRow("界面缩放:", scale_layout)
        
        # Font size
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 24)
        self.font_size_spin.setValue(12)
        self.font_size_spin.setStyleSheet(self.get_spinbox_style())
        theme_layout.addRow("字体大小:", self.font_size_spin)
        
        layout.addWidget(theme_group)
        
        # Window behavior
        window_group = QGroupBox("🖥️ 窗口行为")
        window_group.setStyleSheet(self.get_group_style())
        window_layout = QVBoxLayout(window_group)
        window_layout.setSpacing(15)
        
        self.remember_size_cb = QCheckBox("记住窗口大小和位置")
        self.remember_size_cb.setStyleSheet(self.get_checkbox_style())
        window_layout.addWidget(self.remember_size_cb)
        
        self.start_maximized_cb = QCheckBox("启动时最大化")
        self.start_maximized_cb.setStyleSheet(self.get_checkbox_style())
        window_layout.addWidget(self.start_maximized_cb)
        
        self.always_on_top_cb = QCheckBox("始终置顶")
        self.always_on_top_cb.setStyleSheet(self.get_checkbox_style())
        window_layout.addWidget(self.always_on_top_cb)
        
        layout.addWidget(window_group)
        
        # Animations
        anim_group = QGroupBox("✨ 动画效果")
        anim_group.setStyleSheet(self.get_group_style())
        anim_layout = QVBoxLayout(anim_group)
        anim_layout.setSpacing(15)
        
        self.enable_animations_cb = QCheckBox("启用界面动画")
        self.enable_animations_cb.setChecked(True)
        self.enable_animations_cb.setStyleSheet(self.get_checkbox_style())
        anim_layout.addWidget(self.enable_animations_cb)
        
        self.progress_anim_cb = QCheckBox("进度条动画")
        self.progress_anim_cb.setChecked(True)
        self.progress_anim_cb.setStyleSheet(self.get_checkbox_style())
        anim_layout.addWidget(self.progress_anim_cb)
        
        layout.addWidget(anim_group)
        
        layout.addStretch()
        
        # 添加外观标签页，使用图标
        try:
            from src.qt_icons import get_qicon
            appearance_icon = get_qicon("appearance")
            if not appearance_icon.isNull():
                self.tab_widget.addTab(tab, appearance_icon, " 外观")
            else:
                self.tab_widget.addTab(tab, "🎨 外观")
        except:
            self.tab_widget.addTab(tab, "🎨 外观")
        
    def create_advanced_tab(self):
        """Create advanced settings tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Processing
        proc_group = QGroupBox("🔧 处理选项")
        proc_group.setStyleSheet(self.get_group_style())
        proc_layout = QVBoxLayout(proc_group)
        proc_layout.setSpacing(15)
        
        self.preserve_metadata_cb = QCheckBox("默认保留元数据")
        self.preserve_metadata_cb.setStyleSheet(self.get_checkbox_style())
        proc_layout.addWidget(self.preserve_metadata_cb)
        
        self.backup_original_cb = QCheckBox("处理前备份原文件")
        self.backup_original_cb.setStyleSheet(self.get_checkbox_style())
        proc_layout.addWidget(self.backup_original_cb)
        
        self.smart_mode_cb = QCheckBox("智能模式 (自动选择最佳设置)")
        self.smart_mode_cb.setStyleSheet(self.get_checkbox_style())
        proc_layout.addWidget(self.smart_mode_cb)
        
        layout.addWidget(proc_group)
        
        # File handling
        file_group = QGroupBox("📁 文件处理")
        file_group.setStyleSheet(self.get_group_style())
        file_layout = QVBoxLayout(file_group)
        file_layout.setSpacing(15)
        
        self.skip_small_cb = QCheckBox("跳过小于指定大小的文件")
        self.skip_small_cb.setStyleSheet(self.get_checkbox_style())
        file_layout.addWidget(self.skip_small_cb)
        
        size_layout = QHBoxLayout()
        self.small_size_spin = QSpinBox()
        self.small_size_spin.setRange(1, 1000)
        self.small_size_spin.setValue(10)
        self.small_size_spin.setSuffix(" KB")
        self.small_size_spin.setStyleSheet(self.get_spinbox_style())
        size_layout.addWidget(self.small_size_spin)
        file_layout.addLayout(size_layout)
        
        self.skip_processed_cb = QCheckBox("跳过已优化的文件")
        self.skip_processed_cb.setStyleSheet(self.get_checkbox_style())
        file_layout.addWidget(self.skip_processed_cb)
        
        layout.addWidget(file_group)
        
        # Logging
        log_group = QGroupBox("📝 日志设置")
        log_group.setStyleSheet(self.get_group_style())
        log_layout = QVBoxLayout(log_group)
        log_layout.setSpacing(15)
        
        self.verbose_log_cb = QCheckBox("详细日志模式")
        self.verbose_log_cb.setStyleSheet(self.get_checkbox_style())
        log_layout.addWidget(self.verbose_log_cb)
        
        self.save_log_cb = QCheckBox("保存处理日志到文件")
        self.save_log_cb.setStyleSheet(self.get_checkbox_style())
        log_layout.addWidget(self.save_log_cb)
        
        log_dir_layout = QHBoxLayout()
        self.log_dir_edit = QLineEdit()
        self.log_dir_edit.setPlaceholderText("日志保存目录")
        self.log_dir_edit.setStyleSheet(self.get_lineedit_style())
        log_dir_layout.addWidget(self.log_dir_edit)
        
        log_dir_btn = QPushButton("📁 浏览")
        log_dir_btn.setStyleSheet(self.get_button_style("#3498db"))
        log_dir_btn.clicked.connect(self.browse_log_dir)
        log_dir_layout.addWidget(log_dir_btn)
        
        log_layout.addLayout(log_dir_layout)
        
        layout.addWidget(log_group)
        
        # Reset button
        reset_layout = QHBoxLayout()
        reset_layout.addStretch()
        
        reset_btn = QPushButton("🔄 重置为默认设置")
        reset_btn.setStyleSheet(self.get_button_style("#e74c3c"))
        reset_btn.clicked.connect(self.reset_settings)
        reset_layout.addWidget(reset_btn)
        
        layout.addLayout(reset_layout)
        
        # 添加高级标签页，使用图标
        try:
            advanced_icon = get_qicon("advanced")
            if not advanced_icon.isNull():
                self.tab_widget.addTab(tab, advanced_icon, " 高级")
            else:
                self.tab_widget.addTab(tab, "🔧 高级")
        except:
            self.tab_widget.addTab(tab, "🔧 高级")
        
    def create_button_bar(self, layout):
        """Create button bar"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        # Apply button
        apply_btn = QPushButton("✅ 应用")
        apply_btn.setStyleSheet(self.get_button_style("#27ae60", "large"))
        apply_btn.clicked.connect(self.apply_settings)
        button_layout.addWidget(apply_btn)
        
        # Cancel button
        cancel_btn = QPushButton("❌ 取消")
        cancel_btn.setStyleSheet(self.get_button_style("#95a5a6", "large"))
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        # OK button
        ok_btn = QPushButton("👌 确定")
        ok_btn.setStyleSheet(self.get_button_style("#3498db", "large"))
        ok_btn.clicked.connect(self.accept_settings)
        button_layout.addWidget(ok_btn)
        
        layout.addLayout(button_layout)
        
    def setup_style(self):
        """Setup dialog style"""
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #ecf0f1);
            }
        """)
        
    def get_group_style(self):
        """Get group box style"""
        return """
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                border: 2px solid #3498db;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
                background: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px 0 10px;
                background: white;
            }
        """
        
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
                min-width: 150px;
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
                min-width: 100px;
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
        
    def browse_log_dir(self):
        """Browse for log directory"""
        directory = QFileDialog.getExistingDirectory(self, "选择日志目录")
        if directory:
            self.log_dir_edit.setText(directory)
            
    def load_settings(self):
        """Load settings from config"""
        if not self.config_manager:
            return
            
        try:
            # General settings
            self.lang_combo.setCurrentText("English" if self.config_manager.get("language", "Chinese") == "English" else "中文")
            self.check_updates_cb.setChecked(self.config_manager.get("check_updates", True))
            self.auto_updates_cb.setChecked(self.config_manager.get("auto_updates", False))
            self.associate_cb.setChecked(self.config_manager.get("file_associations", False))
            
            # Optimization settings
            self.default_quality_spin.setValue(self.config_manager.get("quality", 85))
            self.lossless_quality_spin.setValue(self.config_manager.get("lossless_quality", 100))
            self.default_workers_spin.setValue(self.config_manager.get("workers", 4))
            self.memory_limit_spin.setValue(self.config_manager.get("memory_limit", 1024))
            
            fmt = self.config_manager.get("format", "Keep Original")
            self.default_format_combo.setCurrentText("jpg" if fmt == "jpg" else "png" if fmt == "png" else "webp" if fmt == "webp" else "保持原格式")
            
            # Appearance settings
            self.scale_slider.setValue(int(self.config_manager.get("ui_scale", 1.0) * 100))
            self.font_size_spin.setValue(self.config_manager.get("font_size", 12))
            self.remember_size_cb.setChecked(self.config_manager.get("remember_size", True))
            self.start_maximized_cb.setChecked(self.config_manager.get("start_maximized", False))
            self.always_on_top_cb.setChecked(self.config_manager.get("always_on_top", False))
            self.enable_animations_cb.setChecked(self.config_manager.get("enable_animations", True))
            self.progress_anim_cb.setChecked(self.config_manager.get("progress_animations", True))
            
            # Advanced settings
            self.preserve_metadata_cb.setChecked(self.config_manager.get("preserve_metadata", False))
            self.backup_original_cb.setChecked(self.config_manager.get("backup_original", False))
            self.smart_mode_cb.setChecked(self.config_manager.get("smart_mode", False))
            self.skip_small_cb.setChecked(self.config_manager.get("skip_small", False))
            self.small_size_spin.setValue(self.config_manager.get("small_size_threshold", 10))
            self.skip_processed_cb.setChecked(self.config_manager.get("skip_processed", True))
            self.verbose_log_cb.setChecked(self.config_manager.get("verbose_log", False))
            self.save_log_cb.setChecked(self.config_manager.get("save_log", False))
            
            log_dir = self.config_manager.get("log_directory", "")
            if log_dir:
                self.log_dir_edit.setText(log_dir)
                
        except Exception as e:
            print(f"Settings loading warning: {e}")
            
    def save_settings(self):
        """Save settings to config"""
        if not self.config_manager:
            return
            
        try:
            # General settings
            self.config_manager.set("language", "English" if self.lang_combo.currentText() == "English" else "Chinese")
            self.config_manager.set("check_updates", self.check_updates_cb.isChecked())
            self.config_manager.set("auto_updates", self.auto_updates_cb.isChecked())
            self.config_manager.set("file_associations", self.associate_cb.isChecked())
            
            # Optimization settings
            self.config_manager.set("quality", self.default_quality_spin.value())
            self.config_manager.set("lossless_quality", self.lossless_quality_spin.value())
            self.config_manager.set("workers", self.default_workers_spin.value())
            self.config_manager.set("memory_limit", self.memory_limit_spin.value())
            
            fmt = self.default_format_combo.currentText()
            self.config_manager.set("format", "jpg" if fmt == "jpg" else "png" if fmt == "png" else "webp" if fmt == "webp" else "Keep Original")
            
            # Appearance settings
            self.config_manager.set("ui_scale", self.scale_slider.value() / 100.0)
            self.config_manager.set("font_size", self.font_size_spin.value())
            self.config_manager.set("remember_size", self.remember_size_cb.isChecked())
            self.config_manager.set("start_maximized", self.start_maximized_cb.isChecked())
            self.config_manager.set("always_on_top", self.always_on_top_cb.isChecked())
            self.config_manager.set("enable_animations", self.enable_animations_cb.isChecked())
            self.config_manager.set("progress_animations", self.progress_anim_cb.isChecked())
            
            # Advanced settings
            self.config_manager.set("preserve_metadata", self.preserve_metadata_cb.isChecked())
            self.config_manager.set("backup_original", self.backup_original_cb.isChecked())
            self.config_manager.set("smart_mode", self.smart_mode_cb.isChecked())
            self.config_manager.set("skip_small", self.skip_small_cb.isChecked())
            self.config_manager.set("small_size_threshold", self.small_size_spin.value())
            self.config_manager.set("skip_processed", self.skip_processed_cb.isChecked())
            self.config_manager.set("verbose_log", self.verbose_log_cb.isChecked())
            self.config_manager.set("save_log", self.save_log_cb.isChecked())
            
            log_dir = self.log_dir_edit.text().strip()
            if log_dir:
                self.config_manager.set("log_directory", log_dir)
                
            self.config_manager.save()
            
        except Exception as e:
            print(f"Settings saving warning: {e}")
            
    def apply_settings(self):
        """Apply settings without closing dialog"""
        self.save_settings()
        self.settings_changed.emit()
        QMessageBox.information(self, "设置", "设置已应用！")
        
    def accept_settings(self):
        """Accept and close dialog"""
        self.save_settings()
        self.settings_changed.emit()
        self.accept()
        
    def reset_settings(self):
        """Reset all settings to defaults"""
        reply = QMessageBox.question(
            self, "重置设置", 
            "确定要重置所有设置为默认值吗？\n此操作无法撤销。",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Reset to defaults
            self.lang_combo.setCurrentText("中文")
            self.check_updates_cb.setChecked(True)
            self.auto_updates_cb.setChecked(False)
            self.associate_cb.setChecked(False)
            
            self.default_quality_spin.setValue(85)
            self.lossless_quality_spin.setValue(100)
            self.default_workers_spin.setValue(4)
            self.memory_limit_spin.setValue(1024)
            self.default_format_combo.setCurrentText("保持原格式")
            
            self.scale_slider.setValue(100)
            self.font_size_spin.setValue(12)
            self.remember_size_cb.setChecked(True)
            self.start_maximized_cb.setChecked(False)
            self.always_on_top_cb.setChecked(False)
            self.enable_animations_cb.setChecked(True)
            self.progress_anim_cb.setChecked(True)
            
            self.preserve_metadata_cb.setChecked(False)
            self.backup_original_cb.setChecked(False)
            self.smart_mode_cb.setChecked(False)
            self.skip_small_cb.setChecked(False)
            self.small_size_spin.setValue(10)
            self.skip_processed_cb.setChecked(True)
            self.verbose_log_cb.setChecked(False)
            self.save_log_cb.setChecked(False)
            self.log_dir_edit.clear()
            
            QMessageBox.information(self, "重置完成", "所有设置已重置为默认值！")