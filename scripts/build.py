#!/usr/bin/env python3
"""
Build script for TerryOptImg - Qt Version
"""
import os
import subprocess
import sys
import shutil
from pathlib import Path

def build_app():
    """Build the Qt-based TerryOptImg application"""
    print("🔨 Building TerryOptImg (Qt Version)...")
    
    # Create build directory
    build_dir = Path("build")
    build_dir.mkdir(exist_ok=True)
    
    # Copy source files
    print("📁 Copying source files...")
    src_dir = Path("src")
    for file in src_dir.rglob("*.py"):
        if file.is_file():
            dest = build_dir / file.relative_to(src_dir)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(file, dest)
    
    # Copy assets
    assets_dir = Path("assets")
    if assets_dir.exists():
        print("🖼️ Copying assets...")
        for file in assets_dir.rglob("*"):
            if file.is_file():
                dest = build_dir / file.relative_to(assets_dir)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file, dest)
    
    # Copy requirements
    requirements_file = Path("requirements.txt")
    if requirements_file.exists():
        shutil.copy2(requirements_file, build_dir / "requirements.txt")
    
    # Create Qt-specific launcher
    launcher_content = '''#!/usr/bin/env python3
"""
TerryOptImg Qt Launcher
"""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from qt_image_optimizer import main
    main()
except ImportError as e:
    print(f"❌ 启动错误: {e}")
    print("请确保已安装PyQt5: pip install PyQt5")
    sys.exit(1)
'''
    
    launcher_file = build_dir / "run_qt.py"
    with open(launcher_file, 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    # Make launcher executable
    launcher_file.chmod(0o755)
    
    print("✅ Build completed!")
    print(f"📦 Build directory: {build_dir.absolute()}")
    print(f"🚀 Qt启动器: {launcher_file.absolute()}")

if __name__ == "__main__":
    build_app()
