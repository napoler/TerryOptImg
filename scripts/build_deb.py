#!/usr/bin/env python3
"""
Build DEB package for TerryOptImg - Qt Version
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_deb():
    """Build DEB package"""
    print("📦 Building DEB package (Qt Version)...")
    
    # Check if dpkg-deb is available
    try:
        subprocess.run(['which', 'dpkg-deb'], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("❌ dpkg-deb not found. Please install: sudo apt install dpkg-dev")
        return False
    
    # Clean up previous build
    temp_dir = Path("temp_deb")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(exist_ok=True)
    
    # Create directory structure
    usr_bin = temp_dir / "usr" / "bin"
    usr_share_apps = temp_dir / "usr" / "share" / "applications"
    usr_share_icons = temp_dir / "usr" / "share" / "icons" / "hicolor" / "256x256" / "apps"
    opt_dir = temp_dir / "opt" / "terryoptimg"
    
    for directory in [usr_bin, usr_share_apps, usr_share_icons, opt_dir]:
        directory.mkdir(parents=True, exist_ok=True)
    
    # Copy source files to /opt
    src_dir = Path("src")
    for file in src_dir.rglob("*.py"):
        if file.is_file():
            dest = opt_dir / file.relative_to(src_dir)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, dest)
    
    # Copy assets to /opt
    assets_dir = Path("assets")
    if assets_dir.exists():
        for file in assets_dir.rglob("*"):
            if file.is_file():
                dest = opt_dir / file.relative_to(assets_dir)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file, dest)
    
    # Copy requirements
    requirements_file = Path("requirements.txt")
    if requirements_file.exists():
        shutil.copy2(requirements_file, opt_dir / "requirements.txt")
    
    # Copy test script
    test_script = Path("test_desktop.py")
    if test_script.exists():
        shutil.copy2(test_script, opt_dir / "test_desktop.py")
    
    # Create launcher script
    launcher_content = """#!/usr/bin/env python3
import sys
import os

# Set GUI application name for proper desktop integration
os.environ['QT_WM_CLASS'] = 'TerryOptImg'

# Add application path
sys.path.insert(0, '/opt/terryoptimg')

try:
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("TerryOptImg")
    app.setApplicationDisplayName("TerryOptImg")
    app.setDesktopFileName("terryoptimg.desktop")
    
    from qt_image_optimizer import ModernImageOptimizer
    
    window = ModernImageOptimizer()
    window.show()
    
    sys.exit(app.exec_())
    
except ImportError as e:
    from PyQt5.QtWidgets import QMessageBox
    import sys
    
    app = QApplication(sys.argv)
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle("启动错误")
    msg.setText("无法启动TerryOptImg")
    msg.setInformativeText(f"缺少依赖库: {e}\\n\\n请安装依赖:\\nsudo apt install python3-pyqt5 python3-pil")
    msg.exec_()
    sys.exit(1)
except Exception as e:
    from PyQt5.QtWidgets import QMessageBox
    import sys
    
    app = QApplication(sys.argv)
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle("启动错误")
    msg.setText("TerryOptImg启动失败")
    msg.setInformativeText(f"错误详情: {e}")
    msg.exec_()
    sys.exit(1)
"""
    
    launcher_path = usr_bin / "terryoptimg"
    with open(launcher_path, 'w') as f:
        f.write(launcher_content)
    launcher_path.chmod(0o755)
    
    # Copy icon
    icon_path = Path("assets/icon.png")
    if icon_path.exists():
        shutil.copy2(icon_path, usr_share_icons / "terryoptimg.png")
    
    # Create desktop file
    desktop_content = """[Desktop Entry]
Version=1.0
Type=Application
Name=TerryOptImg
Name[zh_CN]=TerryOptImg 图像优化器
Comment=Professional Image Optimizer with Modern Qt Interface
Comment[zh_CN]=专业的图像优化工具，支持有损和无损压缩
Exec=terryoptimg
Icon=terryoptimg
Terminal=false
StartupNotify=true
StartupWMClass=TerryOptImg
Categories=Graphics;Photography;
Keywords=image;optimizer;compression;graphics;图像;优化;压缩;
MimeType=image/png;image/jpeg;image/jpg;image/webp;image/bmp;image/tiff;
"""
    
    desktop_path = usr_share_apps / "terryoptimg.desktop"
    with open(desktop_path, 'w') as f:
        f.write(desktop_content)
    
    # Create DEBIAN directory and control file
    debian_dir = temp_dir / "DEBIAN"
    debian_dir.mkdir(exist_ok=True)
    
    control_content = """Package: terryoptimg
Version: 2.0.0
Section: graphics
Priority: optional
Architecture: all
Depends: python3, python3-pil, python3-pyqt5
Maintainer: Terry <napoler2008@gmail.com>
Description: Professional Image Optimizer with Modern Qt GUI
 A powerful image optimization tool with both lossy and lossless
 compression support. Features a modern PyQt5-based interface.
"""
    
    with open(debian_dir / "control", 'w') as f:
        f.write(control_content)
    
    # Build DEB package
    try:
        result = subprocess.run(['dpkg-deb', '--build', str(temp_dir)], 
                              check=True, capture_output=True, text=True)
        print("✅ DEB package built successfully!")
        print(f"📦 Package: {temp_dir.name}.deb")
        
        # Move deb to dist directory
        dist_dir = Path("dist")
        dist_dir.mkdir(exist_ok=True)
        deb_file = Path(f"{temp_dir.name}.deb")
        if deb_file.exists():
            shutil.move(str(deb_file), dist_dir / "terryoptimg_2.0.0_all.deb")
            print(f"📁 Package moved to: {dist_dir / 'terryoptimg_2.0.0_all.deb'}")
        
        # Cleanup
        shutil.rmtree(temp_dir)
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
        
        # Find the .deb file
        deb_files = list(Path('.').glob('*.deb'))
        if deb_files:
            print(f"📦 DEB package: {deb_files[0].absolute()}")
            return deb_files[0]
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
    
    # Cleanup
    shutil.rmtree(temp_dir)
    return True

if __name__ == "__main__":
    build_deb()
