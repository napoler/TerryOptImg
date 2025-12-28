# 打包指南 (Packaging Guide)

## 简介
本指南介绍如何使用 `PyInstaller` 将 Image Optimizer 打包为独立的可执行文件。

## 前置要求
- 安装 PyInstaller: `pip install pyinstaller`

## 打包步骤

### 1. 自动打包
我们提供了一个构建脚本来简化流程：
```bash
python scripts/build.py
```
构建产物将位于 `dist/` 目录。

### 2. 手动打包
**Windows / Linux**:
```bash
pyinstaller --onefile --windowed --name ImageOptimizer --add-data "src:src" src/image_optimizer_gui.py
```

## 注意事项
- **外部依赖**: 打包后的程序本身不包含 `jpegoptim` 等外部工具。用户仍需将其添加到系统 PATH 或与程序放在同一目录。
- **资源文件**: 如果有图标或其他静态资源，需使用 `--add-data` 参数。
