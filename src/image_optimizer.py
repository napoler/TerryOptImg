import os
import sys
import argparse
import subprocess
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Optional, List, Tuple
from tqdm import tqdm
from PIL import Image

class ImageOptimizer:
    """
    Image Optimizer Logic.
    @spec: FR-001 (Compression), FR-002 (Resize), FR-003 (Conversion)
    """
    def __init__(self, output_dir: Optional[str] = None,
                 max_size: Optional[int] = None,
                 target_format: Optional[str] = None,
                 overwrite: bool = False,
                 quality: int = 85):
        self.output_dir = Path(output_dir) if output_dir else None
        self.max_size = max_size
        self.target_format = target_format.lower() if target_format else None
        self.overwrite = overwrite
        self.quality = quality

        # Check tools
        self.has_jpegoptim = shutil.which('jpegoptim') is not None
        self.has_pngquant = shutil.which('pngquant') is not None
        # cwebp check is optional if we use PIL for webp, but good to have
        self.has_cwebp = shutil.which('cwebp') is not None

    def process_file(self, file_path: Path) -> str:
        try:
            img = Image.open(file_path)

            # Determine output path
            if self.output_dir:
                rel_path = file_path.name
                out_path = self.output_dir / rel_path
                self.output_dir.mkdir(parents=True, exist_ok=True)
            else:
                if not self.overwrite:
                    # Safety: If no output dir and no overwrite, create a default 'optimized' folder?
                    # Or just fail? The prompt implies "replicate Curtail". Curtail overwrites or saves to new folder.
                    # For CLI, let's assume overwrite if flag set, else new folder adjacent
                    parent = file_path.parent
                    out_path = parent / "optimized" / file_path.name
                    out_path.parent.mkdir(exist_ok=True)
                else:
                    out_path = file_path

            # Format conversion logic
            current_ext = file_path.suffix.lower().lstrip('.')
            save_ext = self.target_format if self.target_format else current_ext

            if self.target_format:
                out_path = out_path.with_suffix(f'.{self.target_format}')

            # Resize logic
            if self.max_size:
                w, h = img.size
                if max(w, h) > self.max_size:
                    ratio = self.max_size / max(w, h)
                    new_size = (int(w * ratio), int(h * ratio))
                    img = img.resize(new_size, Image.Resampling.LANCZOS)

            # Save (intermediate or final)
            # If we are converting or resizing, we MUST save via PIL first
            # If inputs match outputs and no resize, we might copy then optimize
            needs_pil_save = (self.max_size is not None) or \
                             (self.target_format is not None and self.target_format != current_ext) or \
                             (not out_path.exists() and out_path != file_path)

            if needs_pil_save:
                # Save using PIL with optimization
                if save_ext in ['jpg', 'jpeg']:
                    img = img.convert('RGB') # JPG doesn't support alpha
                    img.save(out_path, quality=self.quality, optimize=True)
                elif save_ext == 'png':
                    img.save(out_path, optimize=True)
                elif save_ext == 'webp':
                    img.save(out_path, quality=self.quality, method=6)
                else:
                    img.save(out_path)
            elif out_path != file_path:
                 # Just copy if no resize/convert needed but output dir is different
                 shutil.copy2(file_path, out_path)

            # Post-process with external tools if available and file exists
            if out_path.exists():
                self.optimize_external(out_path)

            return f"Processed: {file_path.name}"

        except Exception as e:
            return f"Error {file_path.name}: {str(e)}"

    def optimize_external(self, file_path: Path):
        ext = file_path.suffix.lower()
        if ext in ['.jpg', '.jpeg'] and self.has_jpegoptim:
             subprocess.run(['jpegoptim', '--strip-all', '-m', str(self.quality), str(file_path)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif ext == '.png' and self.has_pngquant:
             # pngquant creates a new file by default, replace it
             subprocess.run(['pngquant', '--force', '--ext', '.png', '--quality', f'65-{self.quality}', str(file_path)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(description="SpecKit Image Optimizer (Curtail Replica)")
    parser.add_argument("input", help="Input file or directory")
    parser.add_argument("--output", "-o", help="Output directory")
    parser.add_argument("--max-size", "-s", type=int, help="Max pixel dimension (resize)")
    parser.add_argument("--format", "-f", help="Target format (jpg, png, webp)")
    parser.add_argument("--workers", "-w", type=int, default=4, help="Concurrency limit")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite input files if no output provided")
    parser.add_argument("--quality", "-q", type=int, default=85, help="Compression quality (0-100)")

    args = parser.parse_args()

    input_path = Path(args.input)
    files = []

    if input_path.is_file():
        files.append(input_path)
    elif input_path.is_dir():
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.webp']:
            files.extend(list(input_path.rglob(ext)))
            files.extend(list(input_path.rglob(ext.upper())))

    if not files:
        print("No image files found.")
        return

    # Create optimizer
    optimizer = ImageOptimizer(
        output_dir=args.output,
        max_size=args.max_size,
        target_format=args.format,
        overwrite=args.overwrite,
        quality=args.quality
    )

    print(f"Processing {len(files)} files with {args.workers} workers...")

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        results = list(tqdm(executor.map(optimizer.process_file, files), total=len(files), unit="img"))

    print("Done.")

if __name__ == "__main__":
    main()
