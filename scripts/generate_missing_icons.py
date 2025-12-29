from PIL import Image, ImageDraw, ImageFont
import os

# Define assets directory
ASSETS_DIR = 'assets'
if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)

# Missing icons identified from previous step
MISSING_ICONS = {
    'folder': {'color': '#3498db', 'text': 'F', 'filename': 'folder.png'},
    'file': {'color': '#95a5a6', 'text': 'f', 'filename': 'file.png'},
    'save': {'color': '#2980b9', 'text': 'S', 'filename': 'save.png'},
    'play': {'color': '#2ecc71', 'text': '>', 'filename': 'play.png'},
    'pause': {'color': '#f39c12', 'text': '||', 'filename': 'pause.png'},
    'cancel': {'color': '#e74c3c', 'text': 'X', 'filename': 'cancel.png'},
    'success': {'color': '#27ae60', 'text': 'V', 'filename': 'success.png'},
    'error': {'color': '#c0392b', 'text': '!', 'filename': 'error.png'},
    'warning': {'color': '#f1c40f', 'text': '!', 'filename': 'warning.png'},
    'info': {'color': '#3498db', 'text': 'i', 'filename': 'info.png'},
    'ready': {'color': '#27ae60', 'text': 'R', 'filename': 'ready.png'},
    'processing': {'color': '#e67e22', 'text': '...', 'filename': 'processing.png'},
    'completed': {'color': '#2ecc71', 'text': 'OK', 'filename': 'completed.png'},
    'failed': {'color': '#e74c3c', 'text': 'F', 'filename': 'failed.png'},
    'progress': {'color': '#3498db', 'text': '%', 'filename': 'progress.png'},
    'log': {'color': '#34495e', 'text': 'L', 'filename': 'log.png'},
    'optimize': {'color': '#9b59b6', 'text': 'O', 'filename': 'optimize.png'},
    'image': {'color': '#1abc9c', 'text': 'I', 'filename': 'image.png'},
    'check': {'color': '#2ecc71', 'text': 'V', 'filename': 'check.png'},
    'close': {'color': '#c0392b', 'text': 'X', 'filename': 'close.png'},
    'refresh': {'color': '#3498db', 'text': 'R', 'filename': 'refresh.png'},
    'download': {'color': '#27ae60', 'text': 'D', 'filename': 'download.png'},
    'upload': {'color': '#3498db', 'text': 'U', 'filename': 'upload.png'},
}

def generate_icon(config):
    size = (64, 64)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw background circle
    draw.ellipse([(2, 2), (62, 62)], fill=config['color'])

    # Draw text
    text = config['text']
    # Approximate text centering without loading external font
    # Font handling in PIL without external files can be tricky, using default or simple logic
    try:
        # Try to load a default font if possible, or use default
        font = ImageFont.load_default()
        # Scale isn't easy with load_default bitmap font.
        # Let's draw shapes for simple ones if we want better look, but text is fallback.
        # For now, let's just draw simple shapes if text is simple

        if text == '>':
            # Play triangle
            draw.polygon([(20, 15), (20, 49), (50, 32)], fill='white')
        elif text == '||':
            # Pause bars
            draw.rectangle([(20, 15), (28, 49)], fill='white')
            draw.rectangle([(36, 15), (44, 49)], fill='white')
        elif text == 'X':
            # Cross
            width = 6
            draw.line((20, 20, 44, 44), fill='white', width=width)
            draw.line((20, 44, 44, 20), fill='white', width=width)
        elif text == '!':
            # Exclamation
            draw.rectangle([(28, 15), (36, 35)], fill='white')
            draw.ellipse([(28, 40), (36, 48)], fill='white')
        elif text == 'i':
            # Info
            draw.ellipse([(28, 15), (36, 23)], fill='white')
            draw.rectangle([(28, 28), (36, 49)], fill='white')
        elif text == '+':
            # Plus
            width = 6
            draw.line((32, 15, 32, 49), fill='white', width=width)
            draw.line((15, 32, 49, 32), fill='white', width=width)
        else:
            # Fallback to drawing text centered-ish
            # Since load_default is small, we might want to manually draw letters or accept small text
            # For this task, getting the file exists is priority.
            # Let's just draw the text with default font (it will be small)
            # Or draw a generic white box in the middle
            bbox = font.getbbox(text)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            x = (64 - w) / 2
            y = (64 - h) / 2
            draw.text((x, y), text, font=font, fill='white')

    except Exception as e:
        print(f"Error drawing {config['filename']}: {e}")

    filepath = os.path.join(ASSETS_DIR, config['filename'])
    img.save(filepath)
    print(f"Generated {filepath}")

def main():
    print("Generating missing icons...")
    for key, config in MISSING_ICONS.items():
        generate_icon(config)
    print("Done.")

if __name__ == "__main__":
    main()
