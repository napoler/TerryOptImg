import os
import sys
import shutil
import subprocess
from pathlib import Path

# Config
APP_NAME = "image-optimizer"
VERSION = "1.1.0"
MAINTAINER = "Terry Chan <napoler2008@gmail.com>"
DESCRIPTION = "Image Optimizer (Curtail Replica)"
DEPENDENCIES = "jpegoptim, pngquant" # Recommended external tools

def build_deb():
    if sys.platform != "linux":
        print("❌ Debian packaging is only supported on Linux.")
        return

    # Check tools
    if not shutil.which("dpkg-deb"):
        print("❌ 'dpkg-deb' not found. Please install 'dpkg'.")
        return

    base_dir = Path(__file__).parent.parent
    dist_dir = base_dir / "dist"
    deb_build_dir = dist_dir / "deb_build"

    # 1. Build Binary
    print("🚀 Building Binary...")
    build_script = base_dir / "scripts" / "build.py"
    subprocess.check_call([sys.executable, str(build_script)])

    # 2. Prepare Directory Structure
    print("🚀 Preparing Debian Structure...")
    if deb_build_dir.exists():
        shutil.rmtree(deb_build_dir)

    usr_bin = deb_build_dir / "usr" / "bin"
    usr_share_apps = deb_build_dir / "usr" / "share" / "applications"
    debian_dir = deb_build_dir / "DEBIAN"

    usr_bin.mkdir(parents=True, exist_ok=True)
    usr_share_apps.mkdir(parents=True, exist_ok=True)
    debian_dir.mkdir(parents=True, exist_ok=True)

    # Install Icon
    icon_dest = deb_build_dir / "usr" / "share" / "icons" / "hicolor" / "256x256" / "apps"
    icon_dest.mkdir(parents=True, exist_ok=True)
    shutil.copy2(base_dir / "assets" / "icon.png", icon_dest / "image-optimizer.png")

    # Copy Binary
    # build.py generates 'ImageOptimizer' in dist/
    binary_src = dist_dir / "ImageOptimizer"
    if not binary_src.exists():
        print(f"❌ Binary not found at {binary_src}. Check build.py output.")
        return

    shutil.copy2(binary_src, usr_bin / APP_NAME)
    # Ensure executable
    os.chmod(usr_bin / APP_NAME, 0o755)

    # 3. Create Control File
    # Note: Architecture is hardcoded to amd64 for this script, but PyInstaller builds for host arch.
    # A robust script would detect arch.
    arch = "amd64"
    control_content = f"""Package: {APP_NAME}
Version: {VERSION}
Section: graphics
Priority: optional
Architecture: {arch}
Depends: {DEPENDENCIES}
Maintainer: {MAINTAINER}
Description: {DESCRIPTION}
 A GUI tool to optimize images (JPG, PNG, WebP, SVG).
 Features smart concurrency and lossless/lossy modes.
"""
    with open(debian_dir / "control", "w") as f:
        f.write(control_content)

    # 4. Create Desktop File
    desktop_content = f"""[Desktop Entry]
Name=Image Optimizer
Comment={DESCRIPTION}
Exec=/usr/bin/{APP_NAME}
Icon=image-optimizer
Terminal=false
Type=Application
Categories=Graphics;Utility;
"""
    with open(usr_share_apps / f"{APP_NAME}.desktop", "w") as f:
        f.write(desktop_content)

    # 5. Build .deb
    print("📦 Packing .deb...")
    deb_filename = f"{APP_NAME}_{VERSION}_{arch}.deb"
    subprocess.check_call(["dpkg-deb", "--build", str(deb_build_dir), str(dist_dir / deb_filename)])

    print(f"✅ Debian Package Created: {dist_dir / deb_filename}")

if __name__ == "__main__":
    build_deb()
