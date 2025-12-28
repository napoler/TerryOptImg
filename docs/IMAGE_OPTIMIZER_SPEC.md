# SpecKit Specification: Image Optimizer (Curtail Replica)

> **版本**: v1.0.0
> **提示词类型**: Image Optimizer Implementation
> **适用场景**: Local Image Compression and Optimization
> **预期效果**: Functional replica of Curtail with GUI and CLI

## 🎯 第一阶段：Constitution (宪法阶段)

### 项目边界宪法
```markdown
# Image Optimizer Constitution

## 核心原则
1. **Functional Replication**: Must replicate key Curtail features (compression, resizing, format conversion).
2. **User Experience**: GUI must be responsive (no freezing) and provide progress feedback.
3. **Data Safety**: Default to non-destructive operations (save to new folder) unless overwrite is explicitly requested.
4. **Performance**: Utilize concurrency for batch processing.

## 技术约束
- **Language**: Python 3.8+
- **GUI Framework**: Tkinter (Standard Library)
- **Dependencies**: Pillow, tqdm (minimal external deps)
- **External Tools**: Support `jpegoptim`, `pngquant` if available, but must function without them.

## 明确不做的事
- ❌ Do not implement complex image editing (cropping, filters) beyond resizing.
- ❌ Do not enforce external tool installation (must fail gracefully/fallback).
```

## 📝 第二阶段：Specification (规范阶段)

### 功能需求清单 (FR-XXX)
```markdown
## Functional Requirements

### FR-001: Image Compression
- Description: Compress JPG, PNG, WebP images.
- Acceptance Criteria: Reduce file size while maintaining visual quality. Use external tools if available.

### FR-002: Image Resizing
- Description: Resize images to a maximum dimension while maintaining aspect ratio.
- Acceptance Criteria: Images exceeding max dimension are downscaled; smaller images are untouched.

### FR-003: Format Conversion
- Description: Convert images between JPG, PNG, WebP.
- Acceptance Criteria: User can select target format.

### FR-004: Graphical User Interface
- Description: Tkinter-based GUI for selecting files/folders and settings.
- Acceptance Criteria: Responsive UI, Progress Bar, Settings controls.

### FR-005: Concurrency
- Description: Process multiple images in parallel.
- Acceptance Criteria: User adjustable worker count, UI remains responsive.
```

## 🏗️ 第三阶段：Plan (计划阶段)

### Architecture Strategy
```python
# Architecture Overview
class ImageOptimizer:
    """Core logic for optimization, decoupled from UI."""
    def process_file(self, path): ...

class OptimizerApp(tk.Tk):
    """GUI Layer."""
    def run_optimizer(self): ...
```

### Implementation Strategy
1.  **Core Logic**: Implement `src/image_optimizer.py` first.
2.  **CLI**: Add `main()` for CLI usage.
3.  **GUI**: Implement `src/image_optimizer_gui.py` consuming `ImageOptimizer`.
4.  **Threading**: Use `concurrent.futures.ThreadPoolExecutor` in the GUI thread handling.

## 📋 第四阶段：Tasks (任务阶段)

### Implementation Tasks
- [x] T-001: Implement `ImageOptimizer` class with resizing and conversion logic.
- [x] T-002: Implement CLI argument parsing.
- [x] T-003: Implement `OptimizerApp` Tkinter GUI.
- [x] T-004: Implement Threading and Queue for UI updates.
- [x] T-005: Verify functionality with test images.
