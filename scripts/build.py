import os
import subprocess
import sys
import shutil
from pathlib import Path

def build():
    print("🚀 Starting Build Process...")

    # Check PyInstaller
    if not shutil.which("pyinstaller"):
        print("❌ PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Define paths
    base_dir = Path(__file__).parent.parent
    src_script = base_dir / "src" / "image_optimizer_gui.py"
    dist_dir = base_dir / "dist"

    # Build command
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", "ImageOptimizer",
        "--clean",
        str(src_script)
    ]

    # OS specific adjustments
    if sys.platform == "win32":
        icon_path = base_dir / "assets" / "icon.ico"
        if icon_path.exists():
            cmd.append(f"--icon={icon_path}")

    print(f"Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=base_dir)

    if result.returncode == 0:
        print(f"✅ Build Successful! Executable in {dist_dir}")
    else:
        print("❌ Build Failed.")

if __name__ == "__main__":
    build()
