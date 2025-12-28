import os
import sys
import argparse
import subprocess
import shutil
import tempfile
import gc
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Optional, List, Tuple, Callable, Dict, Any
from tqdm import tqdm
from PIL import Image, ImageOps
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ImageOptimizer:
    """
    Enhanced Image Optimizer with advanced compression algorithms.
    @spec: FR-001 (Compression), FR-002 (Resize), FR-003 (Conversion)
    """
    def __init__(self, output_dir: Optional[str] = None,
                 max_size: Optional[int] = None,
                 target_format: Optional[str] = None,
                 overwrite: bool = False,
                 quality: int = 85,
                 keep_metadata: bool = False,
                 progress_callback: Optional[Callable[[str, int, int], None]] = None):
        self.output_dir = Path(output_dir) if output_dir else None
        self.max_size = max_size
        self.target_format = target_format.lower() if target_format else None
        self.overwrite = overwrite
        self.quality = quality
        self.keep_metadata = keep_metadata
        self.progress_callback = progress_callback

        # Enhanced tool detection
        self.has_jpegoptim = shutil.which('jpegoptim') is not None
        self.has_pngquant = shutil.which('pngquant') is not None
        self.has_svgo = shutil.which('svgo') is not None
        self.has_scour = shutil.which('scour') is not None
        self.has_optipng = shutil.which('optipng') is not None
        self.has_advpng = shutil.which('advpng') is not None
        self.has_gifsicle = shutil.which('gifsicle') is not None
        self.has_oxipng = shutil.which('oxipng') is not None
        self.has_cwebp = shutil.which('cwebp') is not None
        
        # Log available tools
        available_tools = []
        if self.has_jpegoptim: available_tools.append('jpegoptim')
        if self.has_pngquant: available_tools.append('pngquant')
        if self.has_svgo: available_tools.append('svgo')
        if self.has_scour: available_tools.append('scour')
        if self.has_optipng: available_tools.append('optipng')
        if self.has_advpng: available_tools.append('advpng')
        if self.has_gifsicle: available_tools.append('gifsicle')
        if self.has_oxipng: available_tools.append('oxipng')
        if self.has_cwebp: available_tools.append('cwebp')
        
        logger.info(f"Available optimization tools: {', '.join(available_tools) if available_tools else 'None'}")

    def process_file(self, file_path: Path) -> dict:
        result = {
            "path": str(file_path),
            "success": False,
            "original_size": 0,
            "new_size": 0,
            "message": "",
            "compression_ratio": 0.0
        }
        img = None
        temp_file = None
        
        try:
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")

            result["original_size"] = file_path.stat().st_size
            
            # Notify progress
            if self.progress_callback:
                self.progress_callback(f"Processing {file_path.name}", 0, 100)

            # SVG Handling
            if file_path.suffix.lower() == '.svg':
                return self.process_svg(file_path, result)

            # Load image with memory management
            try:
                img = Image.open(file_path)
                # Convert to RGB if necessary for certain operations
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGBA')
            except Exception as e:
                raise ValueError(f"Cannot load image {file_path.name}: {str(e)}")

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

            # Auto-orient image based on EXIF
            img = ImageOps.exif_transpose(img)
            
            # Resize logic with improved algorithm
            if self.max_size:
                w, h = img.size
                if max(w, h) > self.max_size:
                    ratio = self.max_size / max(w, h)
                    new_size = (int(w * ratio), int(h * ratio))
                    # Use LANCZOS for downsizing, BICUBIC for upsizing
                    resample = Image.Resampling.LANCZOS if ratio < 1 else Image.Resampling.BICUBIC
                    img = img.resize(new_size, resample)
                    
                    if self.progress_callback:
                        self.progress_callback(f"Resized {file_path.name} to {new_size[0]}x{new_size[1]}", 25, 100)

            # Save logic
            save_kwargs = {}
            if self.keep_metadata and 'exif' in img.info:
                save_kwargs['exif'] = img.info['exif']

            needs_pil_save = (self.max_size is not None) or \
                             (self.target_format is not None and self.target_format != current_ext) or \
                             (not out_path.exists() and out_path != file_path)

            if needs_pil_save:
                if save_ext in ['jpg', 'jpeg']:
                    img = img.convert('RGB')
                    img.save(out_path, quality=self.quality, optimize=True, **save_kwargs)
                elif save_ext == 'png':
                    img.save(out_path, optimize=True, **save_kwargs)
                elif save_ext == 'webp':
                    img.save(out_path, quality=self.quality, method=6, **save_kwargs)
                else:
                    img.save(out_path, **save_kwargs)
            elif out_path != file_path:
                 shutil.copy2(file_path, out_path)

            if out_path.exists():
                self.optimize_external(out_path)

            result["success"] = True
            result["new_size"] = out_path.stat().st_size
            result["message"] = f"Processed ({result['original_size']} -> {result['new_size']})"
            return result

        except Exception as e:
            result["message"] = f"Error {file_path.name}: {str(e)}"
            return result

    def process_svg(self, file_path: Path, result: dict) -> dict:
        # SVG logic
        if self.output_dir:
            out_path = self.output_dir / file_path.name
        else:
            out_path = file_path # Overwrite?
            if not self.overwrite:
                 parent = file_path.parent
                 out_path = parent / "optimized" / file_path.name
                 out_path.parent.mkdir(exist_ok=True)

        # Copy first
        if out_path != file_path:
            shutil.copy2(file_path, out_path)

        if self.has_svgo:
            # svgo input output
            cmd = ['svgo', str(out_path)]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif self.has_scour:
            # scour -i in -o out
            cmd = ['scour', '-i', str(out_path), '-o', str(out_path) + '.tmp']
            res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if res.returncode == 0:
                shutil.move(str(out_path) + '.tmp', str(out_path))

        result["success"] = True
        result["new_size"] = out_path.stat().st_size if out_path.exists() else 0
        result["message"] = "SVG Optimized"
        return result

    def optimize_external(self, file_path: Path):
        ext = file_path.suffix.lower()
        if ext in ['.jpg', '.jpeg'] and self.has_jpegoptim:
             cmd = ['jpegoptim', '-m', str(self.quality), str(file_path)]
             if not self.keep_metadata:
                 cmd.append('--strip-all')
             subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif ext == '.png' and self.has_pngquant:
             cmd = ['pngquant', '--force', '--ext', '.png', '--quality', f'65-{self.quality}', str(file_path)]
             if not self.keep_metadata:
                 cmd.append('--strip')
             subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

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
        quality=args.quality,
        keep_metadata=False # CLI default
    )

    print(f"Processing {len(files)} files with {args.workers} workers...")

    total_saved = 0
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        results = list(tqdm(executor.map(optimizer.process_file, files), total=len(files), unit="img"))
        for res in results:
            if res['success']:
                saved = res['original_size'] - res['new_size']
                total_saved += saved

    print(f"Done. Total saved: {total_saved / 1024:.2f} KB")

if __name__ == "__main__":
    main()
