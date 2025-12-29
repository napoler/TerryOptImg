#!/usr/bin/env python3
"""
Qt Icon Resources
提供图标和文本资源
"""
import os
from PyQt5.QtGui import QIcon

# 获取资源目录
def get_assets_path():
    """获取assets目录路径"""
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Check for assets in current directory (for installed package)
    local_assets = os.path.join(current_dir, 'assets')
    if os.path.exists(local_assets):
        return local_assets

    # Check for assets in project root (for dev environment)
    project_root = os.path.dirname(current_dir)
    assets_path = os.path.join(project_root, 'assets')
    return assets_path

# 图标文件路径映射
ICON_FILES = {
    'folder': 'folder.png',
    'file': 'file.png', 
    'add_files': 'add_files.png',
    'add_folder': 'add_folder.png',
    'open': 'open.png',
    'save': 'save.png',
    'settings': 'settings.png',
    'start': 'start.png',
    'stop': 'stop.png',
    'play': 'play.png',
    'pause': 'pause.png',
    'cancel': 'cancel.png',
    'success': 'success.png',
    'error': 'error.png',
    'warning': 'warning.png',
    'info': 'info.png',
    'ready': 'ready.png',
    'processing': 'processing.png',
    'completed': 'completed.png',
    'failed': 'failed.png',
    'logo': 'logo.png',
    'appearance': 'appearance.png',
    'advanced': 'advanced.png',
    'progress': 'progress.png',
    'log': 'log.png',
    'optimize': 'optimize.png',
    'image': 'image.png',
    'check': 'check.png',
    'close': 'close.png',
    'refresh': 'refresh.png',
    'download': 'download.png',
    'upload': 'upload.png',
}

# 图标映射 - 使用Qt内置图标和文本替代
ICON_MAPPING = {
    # 文件操作图标
    'folder': '📁',
    'file': '📄',
    'add_files': '📎',
    'add_folder': '📂',
    'open': '📂',
    'save': '💾',
    'settings': '⚙️',
    
    # 操作图标
    'start': '▶',
    'stop': '⏹',
    'play': '▶️',
    'pause': '⏸️',
    'cancel': '❌',
    'success': '✅',
    'error': '❌',
    'warning': '⚠️',
    'info': 'ℹ️',
    
    # 状态图标
    'ready': '🟢',
    'processing': '🔄',
    'completed': '✅',
    'failed': '❌',
    
    # 界面图标
    'logo': '🎨',
    'progress': '📊',
    'log': '📝',
    'optimize': '⚡',
    'image': '🖼️',
    
    # 其他图标
    'check': '✅',
    'close': '❌',
    'refresh': '🔄',
    'download': '⬇️',
    'upload': '⬆️',
}

# 文本图标映射 - 当表情符号不可用时
TEXT_ICON_MAPPING = {
    'folder': '[文件夹]',
    'file': '[文件]',
    'add_files': '[添加文件]',
    'add_folder': '[添加文件夹]',
    'open': '[打开]',
    'save': '[保存]',
    'settings': '[设置]',
    
    'start': '[开始]',
    'stop': '[停止]',
    'play': '[播放]',
    'pause': '[暂停]',
    'cancel': '[取消]',
    'success': '[成功]',
    'error': '[错误]',
    'warning': '[警告]',
    'info': '[信息]',
    
    'ready': '[就绪]',
    'processing': '[处理中]',
    'completed': '[完成]',
    'failed': '[失败]',
    
    'logo': '[TerryOptImg]',
    'progress': '[进度]',
    'log': '[日志]',
    'optimize': '[优化]',
    'image': '[图片]',
    
    'check': '[确定]',
    'close': '[关闭]',
    'refresh': '[刷新]',
    'download': '[下载]',
    'upload': '[上传]',
}

# Qt标准图标映射
QT_STANDARD_ICONS = {
    'folder': 'SP_DirIcon',
    'file': 'SP_FileIcon',
    'open': 'SP_DialogOpenButton',
    'save': 'SP_DialogSaveButton',
    'settings': 'SP_FileDialogDetailedView',
    'start': 'SP_MediaPlay',
    'stop': 'SP_MediaStop',
    'cancel': 'SP_DialogCancelButton',
    'success': 'SP_DialogApplyButton',
    'error': 'SP_MessageBoxCritical',
    'warning': 'SP_MessageBoxWarning',
    'info': 'SP_MessageBoxInformation',
    'refresh': 'SP_BrowserReload',
    'download': 'SP_ArrowDown',
    'upload': 'SP_ArrowUp',
}

def get_qicon(icon_name, use_standard=True, use_emoji=True):
    """
    获取QIcon对象
    
    Args:
        icon_name: 图标名称
        use_standard: 是否使用Qt标准图标
        use_emoji: 是否使用emoji作为后备（返回QIcon从文本）
    
    Returns:
        QIcon: Qt图标对象
    """
    # 首先尝试从文件加载
    if icon_name in ICON_FILES:
        icon_path = os.path.join(get_assets_path(), ICON_FILES[icon_name])
        if os.path.exists(icon_path):
            return QIcon(icon_path)
    
    # 尝试使用Qt标准图标
    if use_standard and icon_name in QT_STANDARD_ICONS:
        from PyQt5.QtWidgets import QStyle
        from PyQt5.QtWidgets import QApplication
        app = QApplication.instance()
        if app:
            return app.style().standardIcon(getattr(QStyle, QT_STANDARD_ICONS[icon_name]))
    
    # 返回空图标
    return QIcon()

def get_icon(icon_name, use_emoji=True, fallback_text=True, return_qicon=False):
    """
    获取图标
    
    Args:
        icon_name: 图标名称
        use_emoji: 是否使用表情符号
        fallback_text: 是否使用文本作为后备
        return_qicon: 是否返回QIcon对象而不是字符串
    
    Returns:
        QIcon or str: 图标对象或字符串
    """
    if return_qicon:
        return get_qicon(icon_name)
    
    if use_emoji and icon_name in ICON_MAPPING:
        return ICON_MAPPING[icon_name]
    elif fallback_text and icon_name in TEXT_ICON_MAPPING:
        return TEXT_ICON_MAPPING[icon_name]
    else:
        return f"[{icon_name}]"

def get_button_text(text, icon_name=None, use_emoji=True):
    """
    获取按钮文本
    
    Args:
        text: 按钮文本
        icon_name: 图标名称
        use_emoji: 是否使用表情符号
    
    Returns:
        str: 完整的按钮文本
    """
    if icon_name:
        icon = get_icon(icon_name, use_emoji)
        return f"{icon} {text}"
    return text

def get_status_text(status, use_emoji=True):
    """
    获取状态文本
    
    Args:
        status: 状态名称
        use_emoji: 是否使用表情符号
    
    Returns:
        str: 状态文本
    """
    status_mapping = {
        'ready': '就绪',
        'processing': '处理中',
        'completed': '完成',
        'failed': '失败',
        'cancelled': '已取消',
    }
    
    icon = get_icon(status, use_emoji)
    text = status_mapping.get(status, status)
    
    return f"{icon} {text}"

# 颜色映射
STATUS_COLORS = {
    'ready': '#27ae60',
    'processing': '#f39c12',
    'completed': '#27ae60',
    'failed': '#e74c3c',
    'cancelled': '#e74c3c',
    'warning': '#f39c12',
    'error': '#e74c3c',
    'success': '#27ae60',
    'info': '#3498db',
}

def get_status_color(status):
    """获取状态颜色"""
    return STATUS_COLORS.get(status, '#2c3e50')