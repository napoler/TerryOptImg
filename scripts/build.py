#!/usr/bin/env python3
"""
Build script for TerryOptImg using PyInstaller
Generates standalone executables for Windows, Linux, and macOS.
"""
import os
import sys
import shutil
import platform
from pathlib import Path
try:
    import PyInstaller.__main__
except ImportError:
    print("❌ PyInstaller not found. Please install: pip install pyinstaller")
    sys.exit(1)

def build_app():
    """Run PyInstaller build"""
    print(f"🔨 Building TerryOptImg for {platform.system()}...")
    
    # Base directory
    base_dir = Path(__file__).resolve().parent.parent
    src_dir = base_dir / "src"
    assets_dir = base_dir / "assets"
    
    # Determine separator for --add-data
    sep = ';' if platform.system() == 'Windows' else ':'
    
    # Prepare arguments
    args = [
        str(base_dir / "run_qt.py"),  # Entry point
        '--name=TerryOptImg',
        '--onefile',
        '--windowed',
        '--clean',
        '--noconfirm',

        # Paths
        f'--paths={src_dir}',

        # Assets
        f'--add-data={assets_dir}{sep}assets',

        # Hidden imports (Pillow plugins are critical)
        '--hidden-import=PIL',
        '--hidden-import=PIL.TiffImagePlugin',
        '--hidden-import=PIL.JpegImagePlugin',
        '--hidden-import=PIL.PngImagePlugin',
        '--hidden-import=PIL.WebPImagePlugin',
        '--hidden-import=PyQt5',
    ]
    
    # Icon
    if platform.system() == 'Windows':
        icon_path = assets_dir / "icon.ico"
        if icon_path.exists():
            args.append(f'--icon={icon_path}')
    elif platform.system() == 'Darwin':
        icon_path = assets_dir / "icon.icns" # PyInstaller often wants .icns for mac
        if not icon_path.exists():
             # Fallback to png if no icns, though pyinstaller might warn
             icon_path = assets_dir / "icon.png"
        if icon_path.exists():
            args.append(f'--icon={icon_path}')
    else:
        # Linux usually handles icon via .desktop file, but we can embed it
        icon_path = assets_dir / "icon.png"
        if icon_path.exists():
            args.append(f'--icon={icon_path}')

    # Run PyInstaller
    try:
        PyInstaller.__main__.run(args)
        print("✅ Build completed successfully!")

        # Report output location
        dist_dir = base_dir / "dist"
        if platform.system() == 'Windows':
            exe = dist_dir / "TerryOptImg.exe"
            print(f"📦 Output: {exe}")
        else:
            exe = dist_dir / "TerryOptImg"
            print(f"📦 Output: {exe}")

    except Exception as e:
        print(f"❌ Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_app()
