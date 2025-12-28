from PIL import Image, ImageDraw, ImageColor
from pathlib import Path
import os

def generate_icon():
    size = (256, 256)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background: Rounded Rectangle
    color = "#3498db" # Blue
    # Pillow < 8.2 doesn't support rounded_rectangle natively easily without newer features?
    # But 12.0.0 is installed.
    draw.rounded_rectangle([(10, 10), (246, 246)], radius=40, fill=color)

    # Draw "IO" using geometric shapes (Rectangles)
    text_color = "white"

    # I
    draw.rectangle([(60, 60), (90, 196)], fill=text_color)

    # O
    draw.ellipse([(120, 60), (220, 196)], outline=text_color, width=20)

    # Create assets dir
    base_dir = Path(__file__).parent.parent
    assets_dir = base_dir / "assets"
    assets_dir.mkdir(exist_ok=True)

    # Save PNG
    png_path = assets_dir / "icon.png"
    img.save(png_path)
    print(f"Generated {png_path}")

    # Save ICO
    ico_path = assets_dir / "icon.ico"
    # ICO usually needs multiple sizes, but 256x256 is fine for basic
    img.save(ico_path, format='ICO', sizes=[(256, 256)])
    print(f"Generated {ico_path}")

if __name__ == "__main__":
    generate_icon()
